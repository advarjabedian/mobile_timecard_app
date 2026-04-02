from django.contrib import admin

from .models import Employee, PayrollScan


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ["number", "first_name", "last_name", "job_title", "department", "active"]
    list_filter = ["active", "department"]
    search_fields = ["first_name", "last_name", "number"]


@admin.register(PayrollScan)
class PayrollScanAdmin(admin.ModelAdmin):
    list_display = ["employee_id", "scan_date", "scan_time", "working"]
    list_filter = ["working", "scan_date"]
