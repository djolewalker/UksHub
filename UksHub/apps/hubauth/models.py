from django.contrib.auth.models import AbstractUser
from django.db import models
from UksHub.apps.core.validators import path_validator
from django.utils.translation import gettext_lazy as _

# Create your models here.
class User(AbstractUser):
    username = models.CharField(
        max_length=150,
        unique=True,
        help_text= _('Required. 150 characters or fewer. Letters, digits and /-/_ only.'),
        validators=[path_validator],
        error_messages={
            'unique': _("A user with that username already exists."),
        },
    )