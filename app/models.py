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


class Question(models.Model):
    MULTIPLE_CHOICE = 0
    TEXT_INPUT = 1

    QUESTION_TYPE_CHOICES = [
        (MULTIPLE_CHOICE, 'Multiple choice question'),
        (TEXT_INPUT, 'Question with text input')
    ]

    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='questions')
    text = models.CharField(max_length=255, null=False)
    question_type = models.IntegerField(choices=QUESTION_TYPE_CHOICES)


class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers')
    text = models.CharField(max_length=255, null=False)
    is_right = models.BooleanField(default=True)
