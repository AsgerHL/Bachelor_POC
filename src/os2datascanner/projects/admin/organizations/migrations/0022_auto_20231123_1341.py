# Generated by Django 3.2.11 on 2023-11-23 12:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organizations', '0021_organization_msgraph_write_permissions'),
    ]

    operations = [
        migrations.AlterField(
            model_name='organization',
            name='dpotab_access',
            field=models.CharField(choices=[('M', 'Managers'), ('D', 'Data Protection Officers'), ('S', 'Superusers'), ('N', 'None')], default='D', max_length=1, verbose_name='Dpotab access'),
        ),
        migrations.AlterField(
            model_name='organization',
            name='leadertab_access',
            field=models.CharField(choices=[('M', 'Managers'), ('D', 'Data Protection Officers'), ('S', 'Superusers'), ('N', 'None')], default='M', max_length=1, verbose_name='Leadertab access'),
        ),
    ]
