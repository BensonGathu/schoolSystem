# Generated by Django 4.1.1 on 2022-12-19 14:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('systemapp', '0005_alter_leavereportstaff_end_leave_date_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='studentresult',
            name='staff_id',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='systemapp.staffs'),
        ),
    ]