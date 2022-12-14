# Generated by Django 3.2.11 on 2022-11-18 12:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organizations', '0010_alter_position_unit'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='match_count',
            field=models.IntegerField(blank=True, default=0, null=True, verbose_name='Number of matches'),
        ),
        migrations.AddField(
            model_name='account',
            name='match_status',
            field=models.IntegerField(blank=True, choices=[(0, 'Completed'), (1, 'Accepted'), (2, 'Not accepted')], default=1, null=True),
        ),
    ]