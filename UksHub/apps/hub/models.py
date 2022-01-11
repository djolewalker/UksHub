from django.db import models
from django.conf import settings
from UksHub.apps.core.models import TimeStampModel
from easy_thumbnails.fields import ThumbnailerImageField

def user_directory_path(instance, filename):
    return 'avatars/user_{0}/{1}'.format(instance.user.id, filename)

class UserProfile(TimeStampModel):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='userprofile')
    avatar = ThumbnailerImageField(upload_to=user_directory_path, blank=True, null=True)
    name = models.CharField(max_length=400, blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    url = models.URLField(blank=True, null=True)
    twitter = models.CharField(max_length=100, verbose_name='Twitter username', blank=True, null=True)
    company = models.CharField(max_length=200, blank=True, null=True)
    location = models.CharField(max_length=400, blank=True, null=True)