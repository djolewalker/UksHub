from django import forms

from UksHub.apps.hub.models import UserProfile

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('avatar', 'name', 'bio', 'url', 'twitter', 'company', 'location')
