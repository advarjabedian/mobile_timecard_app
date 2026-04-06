from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("timeclock", "0001_initial"),
    ]

    operations = [
        migrations.RunSQL(
            sql="ALTER TABLE payroll_scans ADD COLUMN IF NOT EXISTS day_finished BOOLEAN NOT NULL DEFAULT FALSE;",
            reverse_sql="ALTER TABLE payroll_scans DROP COLUMN IF EXISTS day_finished;",
        ),
    ]
