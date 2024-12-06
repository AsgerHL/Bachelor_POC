from uuid import uuid4
from django.db import models
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from . person import Person

class OffendingDocument(models.Model):

    uuid = models.UUIDField(
        primary_key=True,
        editable=False,
        default=uuid4,
        verbose_name=_('id'),
    )

    persons = models.ManyToManyField(
         Person,
         related_name='offendingdocuments',
         verbose_name=_('persons')
    )

    handle = models.JSONField(
        editable=False,
        verbose_name=_('handle')
    )

    source_age = models.DateTimeField(null=True)
    
class OffendingDocumentSerializer(serializers.ModelSerializer):
    class Meta:
        fields = [
            'uuid',
            'persons',
            'handle',
            'source_age'
            ]

    
   

    
   