# Generated by Django 2.2.10 on 2021-03-05 08:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('os2datascanner_report', '0024_documentreport_resolution_time'),
    ]

    operations = [
        migrations.AddField(
            model_name='documentreport',
            name='created_timestamp',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Created timestamp'),
        ),
    ]
