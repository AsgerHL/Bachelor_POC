# Generated by Django 3.2.11 on 2022-07-28 12:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('os2datascanner', '0085_go_over_to_grants'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='msgraphcalendarscanner',
            name='tenant_id',
        ),
        migrations.RemoveField(
            model_name='msgraphfilescanner',
            name='tenant_id',
        ),
        migrations.RemoveField(
            model_name='msgraphmailscanner',
            name='tenant_id',
        ),
    ]
