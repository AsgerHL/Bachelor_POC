# Generated by Django 3.2.11 on 2023-09-01 11:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organizations', '0021_organization_leadertab_access'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='slug',
            field=models.SlugField(blank=True, null=True),
        ),
    ]
