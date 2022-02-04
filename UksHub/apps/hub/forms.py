from django import forms
from UksHub.apps.hub.models import Issue, PullRequest, UserProfile, Milestone, Label


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('avatar', 'name', 'bio', 'url',
                  'twitter', 'company', 'location')


class IssueForm(forms.ModelForm):
    message = forms.TextInput()

    class Meta:
        model = Issue
        fields = ('name', 'assignees', 'milestone')
        widgets = {'assignees': forms.CheckboxSelectMultiple}


class LabelForm(forms.ModelForm):
    class Meta:
        model = Label
        fields = ('name', 'description', 'color')


class PullRequestForm(forms.ModelForm):
    message = forms.TextInput()

    class Meta:
        model = PullRequest
        fields = ('name', 'assignees', 'milestone')
        widgets = {'assignees': forms.CheckboxSelectMultiple}


class DateInput(forms.DateInput):
    input_type = 'date'


class MilestonesForm(forms.ModelForm):
    class Meta:
        model = Milestone
        fields = ('name', 'description', 'due_date', )
        widgets = {'due_date': DateInput}
