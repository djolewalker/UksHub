from django.db import models
from django.conf import settings
from polymorphic.models import PolymorphicModel
from UksHub.apps.core.enums import BASE_STATE
from UksHub.apps.core.models import TimeStampModel
from UksHub.apps.core.utils import random_hex_color
from UksHub.apps.gitcore.models import Repository
from easy_thumbnails.fields import ThumbnailerImageField
from UksHub.apps.core.validators import path_validator


def user_directory_path(instance, filename):
    return 'avatars/user_{0}/{1}'.format(instance.user.id, filename)


class UserProfile(TimeStampModel):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='userprofile')
    avatar = ThumbnailerImageField(
        upload_to=user_directory_path, blank=True, null=True)
    name = models.CharField(max_length=400, blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    url = models.URLField(blank=True, null=True)
    twitter = models.CharField(
        max_length=100, verbose_name='Twitter username', blank=True, null=True)
    company = models.CharField(max_length=200, blank=True, null=True)
    location = models.CharField(max_length=400, blank=True, null=True)


class Milestone(TimeStampModel):
    name = models.CharField(max_length=100)
    description = models.TextField()
    due_date = models.DateTimeField()
    repository = models.ForeignKey(
        Repository, on_delete=models.CASCADE, null=True)
    is_open = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Artefact(PolymorphicModel):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=250)
    message = models.OneToOneField('events.Comment', blank=True, null=True,
                                   on_delete=models.CASCADE, related_name='%(class)s_messages')
    state = models.BigIntegerField(default=BASE_STATE.OPEN.value)
    repository = models.ForeignKey(Repository, on_delete=models.CASCADE)
    creator = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='%(class)s_creators')
    assignees = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True)
    milestone = models.ForeignKey(
        Milestone, on_delete=models.CASCADE, blank=True, null=True)

    def sorted_event_set(self):
        return self.event_set.order_by('created_at')


class Issue(Artefact):
    pass


class PullRequest(Artefact):
    issues = models.ManyToManyField(Issue)
    target = models.CharField(max_length=200)
    source = models.CharField(max_length=200)
    is_merged = models.BooleanField(default=False)


class Label(TimeStampModel):
    name = models.CharField(max_length=50, unique=True)
    description = models.CharField(max_length=400, blank=True, null=True)
    color = models.CharField(max_length=7, blank=True,
                             null=True, default=random_hex_color)
    repository = models.ForeignKey(
        Repository, on_delete=models.CASCADE, blank=True, null=True)


class ReviewConversation(TimeStampModel):
    review = models.ForeignKey('events.Review', on_delete=models.CASCADE)
    resolved = models.BooleanField()
    file = models.CharField(max_length=400)
    line = models.IntegerField()


class Project(TimeStampModel):
    name = models.CharField(max_length=100)
    description = models.TextField()
    status = models.IntegerField()
    creator = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='creator')
    assignees = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name='assignees')
    repository = models.ForeignKey(Repository, on_delete=models.CASCADE)
    artefacts = models.ManyToManyField(Artefact)


class ProjectColumn(TimeStampModel):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    order = models.IntegerField()
    artefacts = models.ManyToManyField(Artefact)


class Action(TimeStampModel):
    name = models.CharField(max_length=100)
    file = models.CharField(max_length=400)
    disabled = models.BooleanField()
    repository = models.ForeignKey(Repository, on_delete=models.CASCADE)


class WikiPage(TimeStampModel):
    name = models.CharField(max_length=100)


class WikiPageRevision(TimeStampModel):
    page = models.ForeignKey(WikiPage, on_delete=models.CASCADE)
    prev_revision = models.ForeignKey(
        'hub.WikiPageRevision', on_delete=models.CASCADE)
    content = models.TextField()
