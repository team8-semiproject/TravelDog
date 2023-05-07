from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import (
    UserCreationForm, 
    AuthenticationForm, 
    PasswordChangeForm, 
    UsernameField
)
from imagekit.forms import  ProcessedImageField
from imagekit.processors import Thumbnail


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = ("username",)
        field_classes = {'username': UsernameField}


class CustomUserChangeForm(forms.ModelForm):
    picture =  ProcessedImageField(
        spec_id='accounts:profile_picture',
        processors=[Thumbnail(200, 200)],
        format='JPEG',
        options = {'quality':100} 
    )


    class Meta:
        model = get_user_model()
        fields = ('picture',)
 
 
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        password = self.fields.get('password')
        if password:
            password.help_text = password.help_text.format('../password/')
        user_permissions = self.fields.get('user_permissions')
        if user_permissions:
            user_permissions.queryset = user_permissions.queryset.select_related('content_type')


class CustomAuthenticationForm(AuthenticationForm):
    username = UsernameField(
        label='아이디',
        widget=forms.TextInput(
            attrs={
                    'autofocus': True,
                    'placeholder':"username",
                }
            )
        )
    password = forms.CharField(
        label='비밀번호',
        strip=False,
        widget=forms.PasswordInput(
            attrs={
                    'placeholder': "password",
                }
            ),
        )


class CustomPasswordChangeForm(PasswordChangeForm):
    pass

