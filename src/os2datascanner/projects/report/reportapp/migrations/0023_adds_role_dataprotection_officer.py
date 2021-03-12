# Generated by Django 2.2.10 on 2021-01-27 13:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('os2datascanner_report', '0022_adds_role_leader'),
    ]

    operations = [
        migrations.CreateModel(
            name='DataProtectionOfficer',
            fields=[
                ('role_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='os2datascanner_report.Role')),
            ],
            options={
                'verbose_name': 'DPO',
                'verbose_name_plural': "DPO'er",
            },
            bases=('os2datascanner_report.role',),
        ),
    ]
