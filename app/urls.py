# Copyright (c) 2022 Ivan Teplov

from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),

    # quizzes
    path('quiz/new', views.new_quiz, name='new-quiz'),
    path('quiz/<str:quiz_url>', views.quiz_page, name='quiz-page'),
    path('quiz/<str:quiz_url>/add-question', views.add_quiz_question, name='add-quiz-question')
]
