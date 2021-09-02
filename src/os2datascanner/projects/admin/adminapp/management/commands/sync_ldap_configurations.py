#!/usr/bin/env python
# The contents of this file are subject to the Mozilla Public License
# Version 2.0 (the "License"); you may not use this file except in
# compliance with the License. You may obtain a copy of the License at
#    http://www.mozilla.org/MPL/
#
# Software distributed under the License is distributed on an "AS IS"basis,
# WITHOUT WARRANTY OF ANY KIND, either express or implied. See the License
# for the specific language governing rights and limitations under the
# License.
#
# OS2datascanner was developed by Magenta in collaboration with OS2 the
# Danish community of open source municipalities (https://os2.eu/).
#
# The code is currently governed by OS2 the Danish community of open
# source municipalities ( https://os2.eu/ )
from django.core.management import BaseCommand
from django.shortcuts import get_object_or_404
from os2datascanner.projects.admin.core.models.background_job import JobState
from os2datascanner.projects.admin.import_services.models import LDAPConfig, Realm, ImportJob

"""
    This command should be run by a cron job at the desired time
    LDAP synchronizations should take place.
"""


class Command(BaseCommand):
    help = "Run LDAP synchronization for all LDAP configurations configured"

    def handle(self, *args, **kwargs):
        for ldapConf in LDAPConfig.objects.all():
            realm = get_object_or_404(Realm, organization_id=ldapConf.pk)

            latest_importjob = realm.importjob.first()
            if not latest_importjob \
                    or latest_importjob.exec_state == JobState.FINISHED \
                    or latest_importjob.exec_state == JobState.FAILED \
                    or latest_importjob.exec_state == JobState.CANCELLED:

                ImportJob.objects.create(
                    realm=realm
                )