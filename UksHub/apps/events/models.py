from django.conf import settings
from django.db import models
from polymorphic.models import PolymorphicModel


class Event(PolymorphicModel):
    created_at = models.DateTimeField(auto_now_add=True)
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='%(class)s_creators')
    is_removal = models.BooleanField(default=False)
    artefact = models.ForeignKey('hub.Artefact', on_delete=models.CASCADE, related_name='%(class)s_set')


class StateChange(Event):
    new_state = models.BigIntegerField()


class NameChange(Event):
    name = models.CharField(max_length=250)


class PullRequestAssignment(Event):
    pull_request = models.ManyToManyField('hub.PullRequest')


class Comment(Event):
    message = models.TextField()
    conversation = models.ForeignKey('hub.ReviewConversation', on_delete=models.CASCADE, blank=True, null=True)


class ReviewRequest(Event):
    reviewer =  models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)


class Review(Event):
    initial_comment = models.OneToOneField(Comment, on_delete=models.CASCADE)
    request = models.OneToOneField(ReviewRequest, on_delete=models.CASCADE, blank=True, null=True)
    state = models.BigIntegerField()


class LabelApplication(Event):
    label = models.ManyToManyField('hub.Label')


class MilestoneAssignment(Event):
    milestone = models.ForeignKey('hub.Milestone', on_delete=models.CASCADE)


class ProjectColumnAssignment(Event):
    project_column = models.ForeignKey('hub.ProjectColumn', on_delete=models.CASCADE)


class UserAssignment(Event):
    users = models.ManyToManyField(settings.AUTH_USER_MODEL)


class ActionCheck(Event):
    action = models.ForeignKey('hub.Action', on_delete=models.CASCADE)
    trigger = models.CharField(max_length=200)


class FileViewedMark(Event):
    file =  models.CharField(max_length=400)
    pull_request = models.ForeignKey("hub.PullRequest", on_delete=models.CASCADE, related_name='pull_requests')