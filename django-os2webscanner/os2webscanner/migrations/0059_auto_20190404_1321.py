# -*- coding: utf-8 -*-
# Generated by Django 1.11.20 on 2019-04-04 11:21
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('os2webscanner', '0058_auto_20190313_1244'),
    ]

    operations = [
        migrations.CreateModel(
            name='TypeStatistics',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type_name', models.CharField(max_length=256)),
                ('count', models.IntegerField(default=0)),
                ('size', models.IntegerField(default=0)),
            ],
        ),
        migrations.AddField(
            model_name='statistic',
            name='relevant_count',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='statistic',
            name='relevant_size',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='statistic',
            name='relevant_unsupported_count',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='statistic',
            name='relevant_unsupported_size',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='statistic',
            name='supported_count',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='statistic',
            name='supported_size',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='typestatistics',
            name='statistic',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='types', to='os2webscanner.Statistic', verbose_name='Statistics'),
        ),
    ]
