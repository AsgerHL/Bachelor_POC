from rest_framework import serializers
from rest_framework.fields import UUIDField
from .....core_organizational_structure.serializer import BaseSerializer
from django.db import models

from models.person import Person
from models.offendingdocument import OffendingDocument

"""class CoreIndexSerializer(BaseSerializer):
    class Meta:
        fields = ["pk", "person", "offendingdocument"]


class IndexSerializer(CoreIndexSerializer):
    person=serializers.PrimaryKeyRelatedField(
        queryset=Person.objects.all(),
        required=True,
        allow_null=False, 
        pk_field=models.CharField
    )

    offendingDocument=serializers.PrimaryKeyRelatedField(
        queryset=OffendingDocument.objects.all(),
        required=True,
        allow_null=False,
        pk_field=models.UUIDField(format='hex_verbose')
    )


class PositionSerializer(Core_PositionSerializer):
    

    account = serializers.PrimaryKeyRelatedField(
        queryset=Account.objects.all(),
        required=True,
        allow_null=False,
        # This will properly serialize uuid.UUID to str:
        pk_field=UUIDField(format='hex_verbose'))

    unit = serializers.PrimaryKeyRelatedField(
        queryset=OrganizationalUnit.objects.all(),
        required=True,
        allow_null=False,
        # This will properly serialize uuid.UUID to str:
        pk_field=UUIDField(format='hex_verbose'))

    class Meta(Core_PositionSerializer.Meta):
        model = Position"""