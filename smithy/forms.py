from django.contrib.auth.forms import UserCreationForm
from django.forms import forms
from django import forms
from .models import Log

class AccountUpdateForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['username'].disabled = True



class DataForm(forms.ModelForm):
    class Meta:
        model = Log
        fields = ['select', 'info', 'sim', 'result']
