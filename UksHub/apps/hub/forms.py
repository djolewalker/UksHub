from django import forms
from django.forms import ModelForm
from UksHub.apps.hub.models import Issue, PullRequest, UserProfile, Milestone


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('avatar', 'name', 'bio', 'url',
                  'twitter', 'company', 'location')


class IssueForm(forms.ModelForm):
    message = forms.TextInput()

    class Meta:
        model = Issue
        fields = ('name', 'assignees')
        widgets = {'assignees': forms.CheckboxSelectMultiple}


class PullRequestForm(forms.ModelForm):
    message = forms.TextInput()

    class Meta:
        model = PullRequest
        fields = ('name', 'assignees')
        widgets = {'assignees': forms.CheckboxSelectMultiple}


class DateInput(forms.DateInput):
    input_type = 'date'


class MilestonesForm(forms.ModelForm):
    class Meta:
        model = Milestone
        fields = ('name', 'description', 'due_date', )
        widgets = {'due_date': DateInput}
