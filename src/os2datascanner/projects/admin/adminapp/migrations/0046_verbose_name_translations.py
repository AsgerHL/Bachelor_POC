# Generated by Django 2.2.18 on 2021-03-25 13:00

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('os2datascanner', '0045_scanstatus_localisation'),
    ]

    operations = [
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
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='groups', to='os2datascanner.Organization', verbose_name='Organization'),
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
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='os2datascanner.Organization', verbose_name='Organization'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, related_name='profile', to=settings.AUTH_USER_MODEL, verbose_name='User'),
        ),
    ]
