from django.db import models
from django.conf import settings

# Create your models here.
class Visit(models.Model):
    path = models.CharField(max_length=240, default='')
    response_code = models.CharField(max_length=3, default='')
    time = models.DateTimeField()
    host = models.CharField(max_length=30)
    session_id = models.CharField(max_length=40, blank=True, null=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, blank=True, null=True)