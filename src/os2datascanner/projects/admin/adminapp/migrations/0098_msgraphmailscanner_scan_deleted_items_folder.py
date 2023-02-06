# Generated by Django 3.2.11 on 2023-01-05 14:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('os2datascanner', '0097_move_url_from_scanner_to_children'),
    ]

    operations = [
        migrations.AddField(
            model_name='msgraphmailscanner',
            name='scan_deleted_items_folder',
            field=models.BooleanField(default=False, help_text='Include emails in the deleted post folder', verbose_name='Scan deleted items folder'),
        ),
    ]