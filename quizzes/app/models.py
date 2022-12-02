# Copyright (c) 2022 Ivan Teplov

from django.contrib.auth import get_user_model
from django.core.validators import MinLengthValidator
from django.db import models
from django.utils.text import slugify


class Quiz(models.Model):
    class Meta:
        db_table = "quizzes"

    creator = models.ForeignKey(get_user_model(), related_name='created_quizzes', on_delete=models.CASCADE)

    name = models.CharField(max_length=255, null=False, validators=[
        MinLengthValidator(3, 'The name of the quiz has to be at least three characters long')
    ])

    description = models.CharField(max_length=500, null=True)

    @property
    def url(self):
        path = str(self.id) + '-' + self.name.lower()
        return slugify(path, allow_unicode=True)


class Question(models.Model):
    class Meta:
        db_table = "quiz_questions"

    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='questions')
    text = models.CharField(max_length=255, null=False, validators=[
        MinLengthValidator(2, 'The question has to be at least two characters long')
    ])


class Answer(models.Model):
    class Meta:
        db_table = "quiz_question_answers"

    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers')
    text = models.CharField(max_length=255, null=False, validators=[
        MinLengthValidator(2, 'The answer has to be at least two characters long')
    ])

    is_right = models.BooleanField(default=True)
