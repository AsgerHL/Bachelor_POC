from django.db import models
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
#from . offendingdocument import OffendingDocument

class Person(models.Model):
    
    cpr = models.CharField(
        primary_key=True,
        editable=False,
        max_length=12,
        verbose_name=_('cpr'),
    )
    
    

class PersonSerializer(serializers.ModelSerializer):
    class Meta:
        fields = [
            'cpr'
            ]
   

    
   
    

    
    
    