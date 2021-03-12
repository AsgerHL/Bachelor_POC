# Generated by Django 2.2.10 on 2021-01-27 13:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('os2datascanner_report', '0021_documentreport_indexing_for_performance'),
    ]

    operations = [
        migrations.CreateModel(
            name='Leader',
            fields=[
                ('role_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='os2datascanner_report.Role')),
            ],
            options={
                'verbose_name': 'leder',
                'verbose_name_plural': 'ledere',
            },
            bases=('os2datascanner_report.role',),
        ),
    ]
