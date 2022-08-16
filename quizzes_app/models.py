# Copyright (c) 2022 Ivan Teplov

from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.text import slugify

import string


class UserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, name, email, password, is_staff=False, is_superuser=False):
        if not name:
            raise ValidationError('Please, specify your name')
        if not email:
            raise ValidationError('Please, specify your email')
        if len(password) < 4:
            raise ValidationError('Password should be at least 4 characters long')

        email = self.normalize_email(email)
        user = self.model(name=name, email=email, is_staff=is_staff, is_superuser=is_superuser)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, name, email, password):
        return self.create_user(name, email, password, is_staff=True, is_superuser=True)



class User(AbstractUser):
    objects = UserManager()

    # We will use email instead of username
    username = None
    USERNAME_FIELD = 'email'

    # We will use just one field for user's name
    first_name = None
    last_name = None

    name = models.CharField(max_length=50)
    email = models.EmailField(primary_key=True, unique=True)

    REQUIRED_FIELDS = ['name']


class Quiz(models.Model):
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255, null=False)
    description = models.CharField(max_length=500, null=True)

    @property
    def url(self):
        return slugify(str(self.id) + '-' + self.name.lower())
