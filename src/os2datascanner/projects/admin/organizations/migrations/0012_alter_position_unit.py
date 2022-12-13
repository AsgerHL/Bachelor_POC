# Generated by Django 3.2.11 on 2022-12-13 10:58

from django.db import migrations
import django.db.models.deletion
import mptt.fields


class Migration(migrations.Migration):

    dependencies = [
        ('organizations', '0011_alias_organizations_alias_account_unique_constraint_'),
    ]

    operations = [
        migrations.AlterField(
            model_name='position',
            name='unit',
            field=mptt.fields.TreeForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='positions', to='organizations.organizationalunit', verbose_name='organizational unit'),
        ),
    ]
