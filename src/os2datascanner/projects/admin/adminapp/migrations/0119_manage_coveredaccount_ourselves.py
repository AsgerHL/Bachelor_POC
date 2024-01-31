# Generated by Django 3.2.11 on 2023-11-13 09:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ('organizations', '0023_alias_organizations_universal_remediator_constraint'),
        ('os2datascanner', '0118_remove_scanner_rules_and_exclusion_rules_fields'),
    ]

    operations = [
        migrations.SeparateDatabaseAndState(
            database_operations=[
                migrations.RunSQL(
                    sql='ALTER TABLE os2datascanner_scanner_covered_accounts RENAME TO os2datascanner_coveredaccount',
                    reverse_sql='ALTER TABLE os2datascanner_coveredaccount RENAME TO os2datascanner_scanner_covered_accounts',
                ),
            ],
            state_operations=[
                migrations.CreateModel(
                    name='CoveredAccount',
                    fields=[
                        ('id',
                         models.AutoField(auto_created=True, primary_key=True, serialize=False,
                                          verbose_name='ID')),
                        ('account', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE,
                                                      to='organizations.account')),
                        ('scanner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE,
                                                      to='os2datascanner.scanner')),
                    ],
                ),
                migrations.AlterField(
                    model_name='scanner',
                    name='covered_accounts',
                    field=models.ManyToManyField(blank=True, related_name='covered_by_scanner',
                                                 through='os2datascanner.CoveredAccount',
                                                 to='organizations.Account',
                                                 verbose_name='covered accounts'),
                ),
                migrations.AddConstraint(
                    model_name='coveredaccount',
                    constraint=models.UniqueConstraint(fields=('scanner', 'account'),
                                                       name='os2datascanner_scanner_c_scanner_id_account_id_ec9ff164_uniq'),
                ),
            ],
        ),
    ]
