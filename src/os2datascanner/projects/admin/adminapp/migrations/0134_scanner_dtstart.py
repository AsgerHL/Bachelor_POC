# Generated by Django 3.2.11 on 2024-09-10 11:32

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('os2datascanner', '0133_rulecategory_model_and_population'),
    ]

    operations = [
        migrations.AddField(
            model_name='scanner',
            name='dtstart',
            field=models.DateField(default=datetime.date.today, verbose_name='schedule start time'),
        ),
    ]