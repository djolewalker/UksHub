from django import forms
from UksHub.apps.hub.models import Issue, UserProfile


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
