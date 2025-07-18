# Generated by Django 5.2.4 on 2025-07-16 00:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('job_tracker', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='jobapplication',
            name='company_name',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='jobapplication',
            name='date_applied',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='jobapplication',
            name='job_title',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='jobapplication',
            name='original_job_description',
            field=models.TextField(blank=True, null=True),
        ),
    ]
