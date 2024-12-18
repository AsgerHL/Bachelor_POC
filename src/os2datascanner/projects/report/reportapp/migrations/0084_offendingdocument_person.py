# Generated by Django 3.2.11 on 2024-12-06 13:04

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('os2datascanner_report', '0083_rename_resolution_choice'),
    ]

    operations = [
        migrations.CreateModel(
            name='Person',
            fields=[
                ('cpr', models.CharField(editable=False, max_length=10, primary_key=True, serialize=False, verbose_name='cpr')),
            ],
        ),
        migrations.CreateModel(
            name='OffendingDocument',
            fields=[
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, verbose_name='id')),
                ('handle', models.JSONField(editable=False, verbose_name='handle')),
                ('source_age', models.DateTimeField(null=True)),
                ('persons', models.ManyToManyField(related_name='offendingdocuments', to='os2datascanner_report.Person', verbose_name='persons')),
            ],
        ),
    ]
