from django import forms
from registration.models import *

class LoginForm(forms.Form):
    email = forms.CharField(label='Email', required=True)
    password = forms.CharField(widget=forms.PasswordInput, label='Password', required=True)

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not User.objects.all().filter(email=email).exists():
            raise forms.ValidationError('Incorrect Email Address')
        return email

    def clean_password(self):
        password = self.cleaned_data.get('password')
        email = self.cleaned_data.get('email')
        if not User.objects.get(email=email).check_password(password):
            raise forms.ValidationError('Incorrect Password')
        return password