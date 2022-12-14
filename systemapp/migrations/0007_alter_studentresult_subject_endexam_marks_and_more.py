# Generated by Django 4.1.1 on 2022-12-19 16:10

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('systemapp', '0006_studentresult_staff_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='studentresult',
            name='subject_endexam_marks',
            field=models.FloatField(blank=True, default=0, null=True, validators=[django.core.validators.MaxValueValidator(70), django.core.validators.MinValueValidator(0)]),
        ),
        migrations.AlterField(
            model_name='studentresult',
            name='subject_exam1_marks',
            field=models.FloatField(blank=True, default=0, null=True, validators=[django.core.validators.MaxValueValidator(30), django.core.validators.MinValueValidator(0)]),
        ),
        migrations.AlterField(
            model_name='studentresult',
            name='subject_exam2_marks',
            field=models.FloatField(blank=True, default=0, null=True, validators=[django.core.validators.MaxValueValidator(30), django.core.validators.MinValueValidator(0)]),
        ),
    ]
