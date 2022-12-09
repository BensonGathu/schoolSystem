# Generated by Django 4.1.1 on 2022-12-09 08:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('systemapp', '0003_staffs_profile_pic'),
    ]

    operations = [
        migrations.CreateModel(
            name='leave_types',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250)),
            ],
        ),
        migrations.AddField(
            model_name='leavereportstaff',
            name='leave_type',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='systemapp.leave_types'),
            preserve_default=False,
        ),
    ]
