# Generated by Django 4.1.1 on 2022-12-09 09:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('systemapp', '0004_leave_types_leavereportstaff_leave_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='leavereportstaff',
            name='end_leave_date',
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name='leavereportstaff',
            name='start_leave_date',
            field=models.DateTimeField(),
        ),
    ]
