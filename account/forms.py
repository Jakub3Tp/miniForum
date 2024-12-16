from django import forms
from models import Console

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

class ConsoleForm(forms.ModelForm):
    class Meta:
        model = Console
        fields = ['nazwa', 'producent', 'data_premiery', 'zdjecie', 'opis']
