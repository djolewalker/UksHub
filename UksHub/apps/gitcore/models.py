from django.db import models
from django.contrib.auth.models import User
from UksHub.apps.core.models import TimeStampModel
from UksHub.apps.core.validators import path_validator

# Create your models here.
class Repository(TimeStampModel):
    name = models.CharField(max_length=250, unique=True, validators=[path_validator])
    creator = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
    contributors = models.ManyToManyField(User, related_name='contributors')
    private = models.BooleanField(default=False)
    archived = models.BooleanField(default=False)

class PublicKey(TimeStampModel):
    name = models.CharField(max_length=200, validators=[path_validator])
    label = models.CharField(max_length=200, blank=True, null=True, validators=[path_validator])
    public_key = models.CharField(max_length=1000)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    archived = models.BooleanField(default=False)
    class Meta:
        unique_together = ('owner', 'label')
