# Generated by Django 4.1.1 on 2022-11-24 06:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('systemapp', '0011_sessionyearmodel_current_students_mothers_email'),
    ]

    operations = [
        migrations.RenameField(
            model_name='classes',
            old_name='sessionperiod',
            new_name='sessionperiod_id',
        ),
        migrations.AlterUniqueTogether(
            name='classes',
            unique_together={('name', 'sessionperiod_id')},
        ),
    ]
