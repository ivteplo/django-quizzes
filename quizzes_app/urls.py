# Copyright (c) 2022 Ivan Teplov

from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),

    # auth
    path('auth/register', views.register, name='register'),
    path('auth/sign-in', views.sign_in, name='sign-in'),
    path('auth/sign-out', views.sign_out, name='sign-out'),

    # quizzes
    path('quiz/new', views.new_quiz, name='new-quiz'),
    path('quiz/<str:quiz_id>', views.quiz_page, name='quiz-page')
]
