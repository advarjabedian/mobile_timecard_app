from rest_framework import serializers

from .models import Employee, PayrollScan


class EmployeeSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()
    schedule = serializers.SerializerMethodField()

    class Meta:
        model = Employee
        fields = [
            "id", "number", "first_name", "last_name", "full_name",
            "job_title", "department", "schedule",
        ]

    def get_full_name(self, obj):
        parts = [obj.first_name or "", obj.mi or "", obj.last_name or ""]
        return " ".join(p for p in parts if p).strip()

    def get_schedule(self, obj):
        return {
            "sunday": {"in": _fmt(obj.sun_in), "out": _fmt(obj.sun_out)},
            "monday": {"in": _fmt(obj.mon_in), "out": _fmt(obj.mon_out)},
            "tuesday": {"in": _fmt(obj.tue_in), "out": _fmt(obj.tue_out)},
            "wednesday": {"in": _fmt(obj.wed_in), "out": _fmt(obj.wed_out)},
            "thursday": {"in": _fmt(obj.thu_in), "out": _fmt(obj.thu_out)},
            "friday": {"in": _fmt(obj.fri_in), "out": _fmt(obj.fri_out)},
            "saturday": {"in": _fmt(obj.sat_in), "out": _fmt(obj.sat_out)},
        }


def _fmt(t):
    if t is None:
        return None
    hour = t.hour % 12 or 12
    minute = t.strftime("%M")
    ampm = "AM" if t.hour < 12 else "PM"
    return f"{hour}:{minute} {ampm}"


class PayrollScanSerializer(serializers.ModelSerializer):
    punch_type = serializers.SerializerMethodField()

    class Meta:
        model = PayrollScan
        fields = ["id", "employee_id", "scan_date", "scan_time", "working", "punch_type"]

    def get_punch_type(self, obj):
        return "Punch In" if obj.working else "Punch Out"
