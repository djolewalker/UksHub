from django import forms
from django.contrib.auth.models import User
from .models import PublicKey, Repository


class KeyForm(forms.ModelForm):
    class Meta:
        model = PublicKey
        fields = ['name', 'label', 'public_key']

class RepositoryForm(forms.ModelForm):
    class Meta:
        model = Repository
        fields = ['name']
        
class RepositoryContributorsForm(forms.ModelForm):
    def __init__(self, user, *args, **kwargs):
        super(RepositoryContributorsForm, self).__init__(*args, **kwargs)
        self.fields['contributors'].queryset = User.objects.exclude(pk=user.id)

    class Meta:
        model = Repository
        fields = ['contributors']

