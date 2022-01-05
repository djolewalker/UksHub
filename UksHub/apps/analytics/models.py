from django.db import models
from django.contrib.auth.models import User
from django.contrib.sessions.models import Session

# Create your models here.
class Visit(models.Model):
    path = models.CharField(max_length=240, default='')
    responseCode = models.CharField(max_length=3, default='')
    time = models.DateTimeField()
    host = models.CharField(max_length=30)
    session_id = models.CharField(max_length=40, blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)