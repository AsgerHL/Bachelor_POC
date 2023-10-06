# Generated by Django 3.2.11 on 2023-10-09 08:05

from django.conf import settings
import django.contrib.postgres.fields.jsonb
from django.db import migrations, models
import django.db.models.deletion
import os2datascanner.projects.admin.adminapp.models.scannerjobs.gmail
import os2datascanner.projects.admin.adminapp.models.scannerjobs.googledrivescanner
import os2datascanner.projects.admin.adminapp.utils
import uuid


class Migration(migrations.Migration):

    replaces = [('os2datascanner', '0040_remove_uuid_null'), ('os2datascanner', '0041_upload_to_paths_20201217_2335'), ('os2datascanner', '0043_service_endpoint_blank_true'), ('os2datascanner', '0044_apikey'), ('os2datascanner', '0045_scanstatus_localisation'), ('os2datascanner', '0046_verbose_name_translations')]

    dependencies = [
        ('os2datascanner', '0039_populate_uuid_values'),
    ]

    operations = [
        migrations.AlterField(
            model_name='organization',
            name='uuid',
            field=models.UUIDField(default=uuid.uuid4, editable=False, unique=True, verbose_name='UUID'),
        ),
        migrations.AlterField(
            model_name='exchangescanner',
            name='userlist',
            field=models.FileField(upload_to=os2datascanner.projects.admin.adminapp.utils.upload_path_exchange_users),
        ),
        migrations.AlterField(
            model_name='gmailscanner',
            name='service_account_file_gmail',
            field=models.FileField(upload_to=os2datascanner.projects.admin.adminapp.utils.upload_path_gmail_service_account, validators=[os2datascanner.projects.admin.adminapp.models.scannerjobs.gmail.GmailScanner.validate_filetype_json]),
        ),
        migrations.AlterField(
            model_name='gmailscanner',
            name='user_emails_gmail',
            field=models.FileField(upload_to=os2datascanner.projects.admin.adminapp.utils.upload_path_gmail_users, validators=[os2datascanner.projects.admin.adminapp.models.scannerjobs.gmail.GmailScanner.validate_filetype_csv]),
        ),
        migrations.AlterField(
            model_name='googledrivescanner',
            name='service_account_file',
            field=models.FileField(upload_to=os2datascanner.projects.admin.adminapp.utils.upload_path_gdrive_service_account, validators=[os2datascanner.projects.admin.adminapp.models.scannerjobs.googledrivescanner.GoogleDriveScanner.validate_filetype_json]),
        ),
        migrations.AlterField(
            model_name='googledrivescanner',
            name='user_emails',
            field=models.FileField(upload_to=os2datascanner.projects.admin.adminapp.utils.upload_path_gdrive_users, validators=[os2datascanner.projects.admin.adminapp.models.scannerjobs.googledrivescanner.GoogleDriveScanner.validate_filetype_csv]),
        ),
        migrations.AlterField(
            model_name='webscanner',
            name='sitemap',
            field=models.FileField(blank=True, upload_to=os2datascanner.projects.admin.adminapp.utils.upload_path_webscan_sitemap, verbose_name='Sitemap Fil'),
        ),
        migrations.AlterField(
            model_name='exchangescanner',
            name='service_endpoint',
            field=models.URLField(blank=True, default='', max_length=256, verbose_name='Service endpoint'),
        ),
        migrations.CreateModel(
            name='APIKey',
            fields=[
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True, verbose_name='UUID')),
                ('scope', models.TextField()),
                ('organization', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='api_keys', to='os2datascanner.organization')),
            ],
            options={
                'verbose_name': 'API key',
            },
        ),
        migrations.AlterModelOptions(
            name='scanstatus',
            options={'verbose_name': 'scan status', 'verbose_name_plural': 'scan statuses'},
        ),
        migrations.AlterField(
            model_name='scanstatus',
            name='explored_sources',
            field=models.IntegerField(null=True, verbose_name='explored sources'),
        ),
        migrations.AlterField(
            model_name='scanstatus',
            name='scan_tag',
            field=django.contrib.postgres.fields.jsonb.JSONField(unique=True, verbose_name='scan tag'),
        ),
        migrations.AlterField(
            model_name='scanstatus',
            name='scanned_objects',
            field=models.IntegerField(null=True, verbose_name='scanned objects'),
        ),
        migrations.AlterField(
            model_name='scanstatus',
            name='scanned_size',
            field=models.BigIntegerField(null=True, verbose_name='size of scanned objects'),
        ),
        migrations.AlterField(
            model_name='scanstatus',
            name='scanner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='statuses', to='os2datascanner.scanner', verbose_name='associated scanner job'),
        ),
        migrations.AlterField(
            model_name='scanstatus',
            name='total_objects',
            field=models.IntegerField(null=True, verbose_name='total objects'),
        ),
        migrations.AlterField(
            model_name='scanstatus',
            name='total_sources',
            field=models.IntegerField(null=True, verbose_name='total sources'),
        ),
        migrations.AlterField(
            model_name='authentication',
            name='domain',
            field=models.CharField(blank=True, default='', max_length=2024, verbose_name='User domain'),
        ),
        migrations.AlterField(
            model_name='authentication',
            name='iv',
            field=models.BinaryField(blank=True, max_length=32, verbose_name='Initialization Vector'),
        ),
        migrations.AlterField(
            model_name='group',
            name='contact_phone',
            field=models.CharField(max_length=256, verbose_name='Phone'),
        ),
        migrations.AlterField(
            model_name='group',
            name='name',
            field=models.CharField(max_length=256, unique=True, verbose_name='Name'),
        ),
        migrations.AlterField(
            model_name='group',
            name='organization',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='groups', to='os2datascanner.organization', verbose_name='Organization'),
        ),
        migrations.AlterField(
            model_name='group',
            name='user_profiles',
            field=models.ManyToManyField(blank=True, related_name='groups', to='os2datascanner.UserProfile', verbose_name='Users'),
        ),
        migrations.AlterField(
            model_name='organization',
            name='contact_phone',
            field=models.CharField(max_length=256, verbose_name='Phone'),
        ),
        migrations.AlterField(
            model_name='organization',
            name='name',
            field=models.CharField(max_length=256, unique=True, verbose_name='Name'),
        ),
        migrations.AlterField(
            model_name='rule',
            name='sensitivity',
            field=models.IntegerField(choices=[(0, 'Notification'), (1, 'Warning'), (2, 'Problem'), (3, 'Critical')], default=2, verbose_name='Følsomhed'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='organization',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='os2datascanner.organization', verbose_name='Organization'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, related_name='profile', to=settings.AUTH_USER_MODEL, verbose_name='User'),
        ),
    ]
