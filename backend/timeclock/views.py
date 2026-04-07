import logging
import zoneinfo

from django.utils import timezone
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Employee, PayrollScan
from .serializers import EmployeeSerializer, PayrollScanSerializer

logger = logging.getLogger(__name__)

LA_TZ = zoneinfo.ZoneInfo("America/Los_Angeles")


def la_now():
    """Return the current datetime in Los Angeles timezone."""
    return timezone.now().astimezone(LA_TZ)


@api_view(["POST"])
def login_by_number(request):
    """Look up an active employee by their employee number."""
    number = request.data.get("number")
    logger.info("[LOGIN] request body=%s", request.data)
    if not number:
        return Response({"error": "Employee number is required."}, status=400)

    try:
        employee = Employee.objects.get(number=int(number), active=True)
    except Employee.DoesNotExist:
        logger.warning("[LOGIN] employee not found for number=%s", number)
        return Response({"error": "Employee not found."}, status=404)
    except (ValueError, TypeError):
        return Response({"error": "Invalid employee number."}, status=400)

    data = EmployeeSerializer(employee).data
    logger.info("[LOGIN] found employee: id=%s number=%s name=%s %s", employee.id, employee.number, employee.first_name, employee.last_name)
    logger.info("[LOGIN] response=%s", data)
    return Response(data)


@api_view(["POST"])
def punch_in(request):
    """Record a punch-in for the employee."""
    employee_number = request.data.get("employee_number")
    if not employee_number:
        return Response({"error": "employee_number is required."}, status=400)

    try:
        emp = Employee.objects.get(number=int(employee_number), active=True)
    except Employee.DoesNotExist:
        return Response({"error": "Employee not found."}, status=404)

    last_scan = PayrollScan.objects.filter(employee_id=emp.id).order_by("-scan_time").first()
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
        employee_id=emp.id,
        scan_date=scan_date,
        scan_time=now,
        working=True,
    )
    return Response(PayrollScanSerializer(scan).data, status=201)


@api_view(["POST"])
def punch_out(request):
    """Punch out: create a new row with working=False."""
    employee_number = request.data.get("employee_number")
    day_finished = request.data.get("day_finished", False)
    if not employee_number:
        return Response({"error": "employee_number is required."}, status=400)

    try:
        emp = Employee.objects.get(number=int(employee_number), active=True)
    except Employee.DoesNotExist:
        return Response({"error": "Employee not found."}, status=404)

    last_scan = PayrollScan.objects.filter(employee_id=emp.id).order_by("-scan_time").first()
    if not last_scan or not last_scan.working:
        return Response({"error": "Not currently punched in."}, status=400)

    now = la_now()
    scan = PayrollScan.objects.create(
        import_run_id=31,
        employee_id=emp.id,
        scan_date=last_scan.scan_date,
        scan_time=now,
        working=False,
        day_finished=bool(day_finished),
    )
    return Response(PayrollScanSerializer(scan).data, status=201)


@api_view(["GET"])
def punch_history(request, employee_number):
    """Get recent punch history for an employee."""
    try:
        emp = Employee.objects.get(number=int(employee_number), active=True)
    except Employee.DoesNotExist:
        return Response({"error": "Employee not found."}, status=404)
    scans = PayrollScan.objects.filter(employee_id=emp.id).order_by("-scan_time")[:50]
    return Response(PayrollScanSerializer(scans, many=True).data)


@api_view(["GET"])
def today_punches(request, employee_number):
    """Get punches for an employee by scan_date. Defaults to today."""
    logger.info("[TODAY] called with employee_number=%s", employee_number)
    try:
        emp = Employee.objects.get(number=int(employee_number), active=True)
    except Employee.DoesNotExist:
        logger.warning("[TODAY] employee not found for number=%s", employee_number)
        return Response({"error": "Employee not found."}, status=404)
    logger.info("[TODAY] resolved to employee id=%s", emp.id)
    date_str = request.query_params.get("date")
    if date_str:
        from datetime import date as dt_date
        scan_date = dt_date.fromisoformat(date_str)
    else:
        scan_date = la_now().date()
    logger.info("[TODAY] querying payroll_scans: employee_id=%s, scan_date=%s", emp.id, scan_date)
    scans = PayrollScan.objects.filter(
        employee_id=emp.id,
        scan_date=scan_date,
    ).order_by("scan_time")
    data = PayrollScanSerializer(scans, many=True).data
    logger.info("[TODAY] returning %d punches: %s", len(data), data)
    return Response(data)


@api_view(["GET"])
def current_status(request, employee_number):
    """Check if an employee is currently punched in or out."""
    logger.info("[STATUS] called with employee_number=%s", employee_number)
    try:
        emp = Employee.objects.get(number=int(employee_number), active=True)
    except Employee.DoesNotExist:
        logger.warning("[STATUS] employee not found for number=%s", employee_number)
        return Response({"error": "Employee not found."}, status=404)
    logger.info("[STATUS] resolved to employee id=%s", emp.id)
    last_scan = PayrollScan.objects.filter(employee_id=emp.id).order_by("-scan_time").first()
    if last_scan:
        data = {
            "is_punched_in": last_scan.working,
            "last_punch": PayrollScanSerializer(last_scan).data,
        }
        logger.info("[STATUS] last_scan id=%s working=%s day_finished=%s scan_date=%s", last_scan.id, last_scan.working, last_scan.day_finished, last_scan.scan_date)
        logger.info("[STATUS] response=%s", data)
        return Response(data)
    logger.info("[STATUS] no scans found for employee_id=%s", emp.id)
    return Response({"is_punched_in": False, "last_punch": None})
