import zoneinfo

from django.utils import timezone
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Employee, PayrollScan
from .serializers import EmployeeSerializer, PayrollScanSerializer

LA_TZ = zoneinfo.ZoneInfo("America/Los_Angeles")


def la_now():
    """Return the current datetime in Los Angeles timezone."""
    return timezone.now().astimezone(LA_TZ)


@api_view(["POST"])
def login_by_number(request):
    """Look up an active employee by their employee number."""
    number = request.data.get("number")
    if not number:
        return Response({"error": "Employee number is required."}, status=400)

    try:
        employee = Employee.objects.get(number=int(number), active=True)
    except Employee.DoesNotExist:
        return Response({"error": "Employee not found."}, status=404)
    except (ValueError, TypeError):
        return Response({"error": "Invalid employee number."}, status=400)

    return Response(EmployeeSerializer(employee).data)


@api_view(["POST"])
def punch_in(request):
    """Record a punch-in for the employee."""
    employee_id = request.data.get("employee_id")
    if not employee_id:
        return Response({"error": "employee_id is required."}, status=400)

    last_scan = PayrollScan.objects.filter(employee_id=int(employee_id)).order_by("-scan_time").first()
    if last_scan and last_scan.working:
        return Response({"error": "Already punched in."}, status=400)

    now = la_now()
    # Returning from break: carry forward the original scan_date
    if last_scan and not last_scan.working and not last_scan.day_finished:
        scan_date = last_scan.scan_date
    else:
        scan_date = now.date()

    scan = PayrollScan.objects.create(
        import_run_id=31,
        employee_id=int(employee_id),
        scan_date=scan_date,
        scan_time=now,
        working=True,
    )
    return Response(PayrollScanSerializer(scan).data, status=201)


@api_view(["POST"])
def punch_out(request):
    """Punch out: create a new row with working=False."""
    employee_id = request.data.get("employee_id")
    day_finished = request.data.get("day_finished", False)
    if not employee_id:
        return Response({"error": "employee_id is required."}, status=400)

    last_scan = PayrollScan.objects.filter(employee_id=int(employee_id)).order_by("-scan_time").first()
    if not last_scan or not last_scan.working:
        return Response({"error": "Not currently punched in."}, status=400)

    now = la_now()
    scan = PayrollScan.objects.create(
        import_run_id=31,
        employee_id=int(employee_id),
        scan_date=last_scan.scan_date,
        scan_time=now,
        working=False,
        day_finished=bool(day_finished),
    )
    return Response(PayrollScanSerializer(scan).data, status=201)


@api_view(["GET"])
def punch_history(request, employee_id):
    """Get recent punch history for an employee."""
    scans = PayrollScan.objects.filter(employee_id=employee_id).order_by("-scan_time")[:50]
    return Response(PayrollScanSerializer(scans, many=True).data)


@api_view(["GET"])
def today_punches(request, employee_id):
    """Get punches for an employee by scan_date. Defaults to today."""
    date_str = request.query_params.get("date")
    if date_str:
        from datetime import date as dt_date
        scan_date = dt_date.fromisoformat(date_str)
    else:
        scan_date = la_now().date()
    scans = PayrollScan.objects.filter(
        employee_id=employee_id,
        scan_date=scan_date,
    ).order_by("scan_time")
    return Response(PayrollScanSerializer(scans, many=True).data)


@api_view(["GET"])
def current_status(request, employee_id):
    """Check if an employee is currently punched in or out."""
    last_scan = PayrollScan.objects.filter(employee_id=employee_id).order_by("-scan_time").first()
    if last_scan:
        return Response({
            "is_punched_in": last_scan.working,
            "last_punch": PayrollScanSerializer(last_scan).data,
        })
    return Response({"is_punched_in": False, "last_punch": None})
