from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.db import models
from friend.models import Friend
from django.utils.translation import gettext_lazy as _
from django.conf import settings


class UserManager(BaseUserManager):

    def create_user(self, email, username, first_name, last_name, password=None):
        if not email:
            raise ValueError(_('Users must have an email address.'))
        if not username:
            raise ValueError(_('Users must have an username.'))
        if not first_name:
            raise ValueError(_('Users must have an firstname.'))
        if not last_name:
            raise ValueError(_('Users must have an lastname.'))
        user = self.model(
            email=self.normalize_email(email),
            username=username,
            first_name=first_name,
            last_name=last_name,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, first_name, last_name, password):
        user = self.create_user(
            email=self.normalize_email(email),
            username=username,
            first_name=first_name,
            last_name=last_name,
            password=password
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


def get_upload_path(instance, field_name):
    return f'images/{instance.pk}/images.png'


def get_default_path():
    return f'images/default.svg'


class User(AbstractBaseUser):
    email = models.EmailField(verbose_name="email", max_length=60, unique=True)
    username = models.CharField(verbose_name="username", max_length=60, unique=True)
    first_name = models.CharField(verbose_name="first_name", max_length=60, blank=False)
    last_name = models.CharField(verbose_name="last_name", max_length=60, blank=False)
    date_joined = models.DateTimeField(verbose_name="date joined", auto_now_add=True)
    last_login = models.DateTimeField(verbose_name="last login", auto_now=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    profile_image = models.ImageField(max_length=255, null=True, blank=True, default=get_default_path,
                                      upload_to=get_upload_path)
    hide_email = models.BooleanField(default=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    def __str__(self):
        return self.username

    def get_profile_image(self):
        return str(self.profile_image)[str(self.profile_image).index(f'images/{self.pk}/'):]

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        friend_object, created = Friend.objects.get_or_create(user=self)
        if created:
            friend_object.save()
