from django import forms
from django.contrib.auth import get_user_model
from .models import PublicKey, Repository


class KeyForm(forms.ModelForm):
    class Meta:
        model = PublicKey
        fields = ['name', 'label', 'public_key']

class RepositoryForm(forms.ModelForm):
    owner = forms.CharField(max_length=500, required=False, disabled=True)
    isPublic = forms.ChoiceField(choices=[
        (True,'Public, anyone on the internet can see this repository. You choose who can commit.'),
        (False,'Private, you choose who can see and commit to this repository.')
        ], widget=forms.RadioSelect, label="")
    class Meta:
        model = Repository
        fields = ['name', 'description']
        
class RepositoryContributorsForm(forms.ModelForm):
    def __init__(self, user, *args, **kwargs):
        super(RepositoryContributorsForm, self).__init__(*args, **kwargs)
        self.fields['contributors'].queryset = get_user_model().objects.exclude(pk=user.id)

    class Meta:
        model = Repository
        fields = ['contributors']

