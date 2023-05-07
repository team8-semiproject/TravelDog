from django.apps import apps
from django.contrib.auth import base_user as auth_models
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models
from django.utils.translation import gettext_lazy as _
from imagekit.models import ProcessedImageField
from imagekit.processors import Thumbnail


class UserManager(auth_models.BaseUserManager):
    def create_user(self, username: str, password: str=None, is_active=False, is_admin=False):
        if not username:
            raise ValueError('The given username must be set')

        GlobalUserModel = apps.get_model(self.model._meta.app_label, self.model._meta.object_name)
        username = GlobalUserModel.normalize_username(username)

        user = self.model(username=username)
        user.set_password(password)
        user.save(using=self._db)
        return user


    def create_superuser(self, username, password):
        user = self.create_user(
            username=username,
            password=password,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class User(auth_models.AbstractBaseUser):
    username_validator = UnicodeUsernameValidator()
    username = models.CharField(
        _('username'),
        max_length=30,
        unique=True,
        help_text=_('Required. 30 characters or fewer. Letters, digits and @/./+/-/_ only.'),
        validators=[username_validator],
        error_messages={
            'unique': _("A user with that username already exists."),
        },
    )
    # user profile picture
    picture = ProcessedImageField(
        blank = True,
        upload_to ='images/users/pictures',
        processors=[Thumbnail(200, 200)], # 처리할 작업목록
        format = 'JPEG', # 최종 저장 포맷
        options = {'quality':100} # 저장 옵션
    )

    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []


    def __str__(self):
        return self.username


    def has_perm(self, perm, obj=None):
        return True


    def has_module_perms(self, app_label):
        return True


    @property
    def is_staff(self):
        return self.is_admin