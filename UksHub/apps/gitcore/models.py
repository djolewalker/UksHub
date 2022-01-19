from django.db import models
from django.conf import settings
from git import Commit as cmt, Head
from UksHub.apps.core.models import TimeStampModel
from UksHub.apps.core.validators import path_validator

# Create your models here.
class Repository(TimeStampModel):
    name = models.CharField(max_length=250, validators=[path_validator])
    description = models.TextField(blank=True, null=True)
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, blank=True, null=True)
    contributors = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='contributors')
    private = models.BooleanField(default=False)
    archived = models.BooleanField(default=False)
    default_branch = models.CharField(max_length=400, default='master')
    
    class Meta:
        unique_together = ('name', 'creator')

class PublicKey(TimeStampModel):
    name = models.CharField(max_length=200, validators=[path_validator])
    label = models.CharField(max_length=200, blank=True, null=True, validators=[path_validator])
    public_key = models.CharField(max_length=1000)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    archived = models.BooleanField(default=False)
    class Meta:
        unique_together = ('owner', 'label')

class Branch(Head):   
    pass

class Commit(cmt):
    pass