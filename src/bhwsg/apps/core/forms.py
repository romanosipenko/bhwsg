from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.models import User


def validateEmail(email):
    from django.core.validators import validate_email
    from django.core.exceptions import ValidationError
    try:
        validate_email(email)
        return True
    except ValidationError:
        return False


class LoginForm(forms.Form):
    username = forms.CharField(required=True)
    password = forms.CharField(required=True, widget=forms.PasswordInput)

    def clean_username(self):
        username = self.cleaned_data['username']
        if '@' in username:
            if validateEmail(username) and User.objects.filter(email=username).exists():
                self.user = User.objects.get(email=username)
            else:
                raise forms.ValidationError("Enter valid email/username or password.")
        else:
            if User.objects.filter(username=username).exists():
                self.user = User.objects.get(username=username)
            else:
                raise forms.ValidationError("Enter valid email/username or password.")
        return username

    def authenticate(self):
        return authenticate(username=self.user.username, password=self.cleaned_data['password'])
