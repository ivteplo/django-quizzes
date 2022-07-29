# Copyright (c) 2022 Ivan Teplov

from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    # We will use email instead of username
    username = None
    USERNAME_FIELD = 'email'

    # We will use just one field for user's name
    first_name = None
    last_name = None

    name = models.CharField(max_length=50)
    email = models.EmailField(primary_key=True, unique=True)

    REQUIRED_FIELDS = []
