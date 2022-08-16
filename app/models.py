# Copyright (c) 2022 Ivan Teplov

from django.contrib.auth import get_user_model
from django.db import models
from django.utils.text import slugify


class Quiz(models.Model):
    creator = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    name = models.CharField(max_length=255, null=False)
    description = models.CharField(max_length=500, null=True)

    @property
    def url(self):
        return slugify(str(self.id) + '-' + self.name.lower())
