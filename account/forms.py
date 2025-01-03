from symtable import Class

from django import forms

from account.models import Console, Comment, Rating
from .models import Profile
from django.contrib.auth import get_user_model

from django.contrib.auth.models import User

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

class ConsoleForm(forms.ModelForm):
    class Meta:
        model = Console
        fields = ['nazwa', 'producent', 'data_premiery', 'zdjecie', 'opis']

class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(label='Hasło',
                               widget=forms.PasswordInput)
    password2 = forms.CharField(label='Powtórz hasło',
                                widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'email')

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise  forms.ValidationError("Hasła nie są takie same")
        return cd['password2']

class UserEditForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields =  ['first_name','last_name','email']

class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['date_of_birth','photo']

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['tresc']

class RatingForm(forms.ModelForm):
    class Meta:
        model = Rating
        fields = ['ocena']
