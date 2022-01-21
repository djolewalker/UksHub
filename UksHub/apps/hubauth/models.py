from django.contrib.auth.models import AbstractUser
from django.db import models
from UksHub.apps.core.models import TimeStampModel
from UksHub.apps.core.validators import path_validator
from django.utils.translation import gettext_lazy as _

# Create your models here.
class User(AbstractUser):
    username = models.CharField(
        max_length=150,
        unique=True,
        help_text= _('Required. 150 characters or fewer. Letters, digits and /-/_/. only.'),
        validators=[path_validator],
        error_messages={
            'unique': _("A user with that username already exists."),
        },
    )


class Email(TimeStampModel):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='emails')
    address = models.EmailField(max_length=254)
    verified = models.BooleanField()
    isPrimary = models.BooleanField()
    isVisible = models.BooleanField()
    isNotification = models.BooleanField()
