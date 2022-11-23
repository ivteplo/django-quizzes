# Copyright (c) 2022 Ivan Teplov

from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('search', views.search, name='search'),
    path('profile', views.profile, name='profile'),

    # quizzes
    path('quiz/new', views.new_quiz, name='new-quiz'),
    path('quiz/<str:quiz_url>', views.quiz_page, name='quiz-page'),
    path('quiz/<str:quiz_url>/edit', views.edit_quiz, name='edit-quiz'),
    path('quiz/<str:quiz_url>/add-question', views.add_quiz_question, name='add-quiz-question'),

    # authentication
    path('auth/register', views.register, name='register'),
    path('auth/sign-in', views.sign_in, name='sign-in'),
    path('auth/sign-out', views.sign_out, name='sign-out')
]
