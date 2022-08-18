# Copyright (c) 2022 Ivan Teplov

from authentication.models import User
from django.db import models
from django.utils.text import slugify


class Quiz(models.Model):
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255, null=False)
    description = models.CharField(max_length=500, null=True)

    @property
    def url(self):
        path = str(self.id) + '-' + self.name.lower()
        return slugify(path, allow_unicode=True)
