# Generated by Django 3.2.11 on 2024-09-12 09:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('import_services', '0024_ldapconfig_group_filter'),
    ]

    operations = [
        migrations.AddField(
            model_name='ldapconfig',
            name='import_managers',
            field=models.BooleanField(default=False, help_text='If true, any imported group with a managedBy attribute will have that user added as a manager', verbose_name='Set managing users as managers'),
        ),
    ]
