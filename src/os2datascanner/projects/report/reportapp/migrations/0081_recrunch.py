# Generated by Django 3.2.11 on 2024-04-23 09:21

from django.db import migrations

from os2datascanner.utils.batch import BatchUpdate
from os2datascanner.engine2.model.core import Handle, Source


def get_crunchable(dr) -> Handle | Source | None:
    if dr.raw_matches:
        return Handle.from_json_object(dr.raw_matches["handle"])
    elif dr.raw_metadata:
        return Handle.from_json_object(dr.raw_metadata["handle"])
    elif dr.raw_problem:
        if dr.raw_problem["handle"]:
            return Handle.from_json_object(dr.raw_problem["handle"])
        else:
            return Source.from_json_object(dr.raw_problem["source"])

    return None


def recrunch(apps, schema_editor):
    DocumentReport = apps.get_model(
            'os2datascanner_report', 'DocumentReport')

    with BatchUpdate(DocumentReport.objects, ["path"]) as batch:
        for report in DocumentReport.objects.order_by("-pk").iterator():
            crunchable = get_crunchable(report)

            if crunchable:
                report.path = crunchable.censor().crunch(hash=True)

                batch.append(report)

    print(f"Updated {batch.count} DocumentReports")


class Migration(migrations.Migration):

    dependencies = [
        ('os2datascanner_report', '0080_remove_defaultrole_and_remediator'),
    ]

    operations = [
        migrations.RunPython(
                recrunch,
                reverse_code=migrations.RunPython.noop)
    ]
