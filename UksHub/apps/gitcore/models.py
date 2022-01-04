from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Repository(models.Model):
    name = models.CharField(max_length=250, unique=True)
    creator = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
    contributors = models.ManyToManyField(User, related_name='contributors')
    private = models.BooleanField(default=False)
    archived = models.BooleanField(default=False)

class PublicKey(models.Model):
    label = models.CharField(max_length=200, blank=True, null=True)
    public_key = models.CharField(max_length=1000)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    archived = models.BooleanField(default=False)
    class Meta:
        unique_together = ('owner', 'label')
