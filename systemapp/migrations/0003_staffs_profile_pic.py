# Generated by Django 4.1.1 on 2022-12-06 09:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('systemapp', '0002_rename_phone_number_staffs_phone'),
    ]

    operations = [
        migrations.AddField(
            model_name='staffs',
            name='profile_pic',
            field=models.FileField(blank=True, null=True, upload_to=''),
        ),
    ]
