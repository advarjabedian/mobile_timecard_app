from django.db import models


class Employee(models.Model):
    id = models.AutoField(primary_key=True)
    import_run_id = models.BigIntegerField(null=True, blank=True)
    company_id = models.BigIntegerField(null=True, blank=True)
    number = models.IntegerField(null=True, blank=True)
    hire_date = models.DateField(null=True, blank=True)
    first_name = models.CharField(max_length=50, blank=True)
    last_name = models.CharField(max_length=50, blank=True)
    mi = models.CharField(max_length=50, blank=True)
    ssno = models.CharField(max_length=50, blank=True)
    phone_number = models.CharField(max_length=50, blank=True)
    mobile_number = models.CharField(max_length=50, blank=True)
    address = models.CharField(max_length=100, blank=True)
    address2 = models.CharField(max_length=100, blank=True)
    city = models.CharField(max_length=50, blank=True)
    state = models.CharField(max_length=50, blank=True)
    zip_code = models.CharField(max_length=20, blank=True)
    hourly = models.BooleanField(default=False)
    hourly_wage = models.DecimalField(max_digits=14, decimal_places=4, null=True, blank=True)
    salary = models.BooleanField(default=False)
    salary_wage = models.DecimalField(max_digits=14, decimal_places=4, null=True, blank=True)
    gender = models.CharField(max_length=50, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    email = models.CharField(max_length=255, blank=True)
    emerg_name = models.CharField(max_length=100, blank=True)
    emerg_phone = models.CharField(max_length=50, blank=True)
    relation = models.CharField(max_length=50, blank=True)
    job_title = models.CharField(max_length=100, blank=True)
    active = models.BooleanField(default=True)
    comments = models.TextField(blank=True)
    alias = models.CharField(max_length=100, blank=True)
    mon_in = models.TimeField(null=True, blank=True)
    mon_out = models.TimeField(null=True, blank=True)
    tue_in = models.TimeField(null=True, blank=True)
    tue_out = models.TimeField(null=True, blank=True)
    wed_in = models.TimeField(null=True, blank=True)
    wed_out = models.TimeField(null=True, blank=True)
    thu_in = models.TimeField(null=True, blank=True)
    thu_out = models.TimeField(null=True, blank=True)
    fri_in = models.TimeField(null=True, blank=True)
    fri_out = models.TimeField(null=True, blank=True)
    sat_in = models.TimeField(null=True, blank=True)
    sat_out = models.TimeField(null=True, blank=True)
    sun_in = models.TimeField(null=True, blank=True)
    sun_out = models.TimeField(null=True, blank=True)
    department = models.CharField(max_length=100, blank=True)
    supervisor_id = models.SmallIntegerField(null=True, blank=True)
    created_at = models.DateTimeField(null=True, blank=True)
    updated_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = "employees"
        managed = False

    def __str__(self):
        return f"{self.first_name} {self.last_name} (#{self.number})"


class PayrollScan(models.Model):
    id = models.AutoField(primary_key=True)
    import_run_id = models.BigIntegerField(null=True, blank=True)
    employee_id = models.IntegerField()
    scan_date = models.DateField(null=True, blank=True)
    scan_time = models.DateTimeField(null=True, blank=True)
    working = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "payroll_scans"
        managed = False
        ordering = ["-scan_time"]

    def __str__(self):
        return f"Employee {self.employee_id} - {self.scan_date} {self.scan_time}"
