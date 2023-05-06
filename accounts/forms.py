from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm, PasswordChangeForm, UsernameField


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = ("username",)
        field_classes = {'username': UsernameField}


class CustomUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = get_user_model()
        fields = '__all__'


class CustomAuthenticationForm(AuthenticationForm):
    username = UsernameField(
        label='',
        widget=forms.TextInput(
            attrs={
                    'autofocus': True,
                    'placeholder':"username",
                }
            )
        )
    password = forms.CharField(
        label='',
        strip=False,
        widget=forms.PasswordInput(
            attrs={
                    'placeholder': "password",
                }
            ),
        )


class CustomPasswordChangeForm(PasswordChangeForm):
    pass