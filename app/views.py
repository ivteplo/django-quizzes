# Copyright (c) 2022 Ivan Teplov

from authentication.decorators import signed_in_only

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.http import HttpRequest, Http404
from django.shortcuts import redirect, render, get_object_or_404

from .models import Quiz


User = get_user_model()


def home(request: HttpRequest):
    latest_quizzes = Quiz.objects.all().order_by('-id')[:10]

    return render(request, 'app/index.html', {
        'latest_quizzes': latest_quizzes
    })


@signed_in_only
def new_quiz(request: HttpRequest):
    options = {}

    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')

        try:
            quiz = Quiz.objects.create(creator=request.user, name=name, description=description)
        except ValidationError as error:
            options['error'] = error
        else:
            return redirect('quiz-page', quiz_url=quiz.id)


    return render(request, 'quiz/new.html', options)


def quiz_page(request: HttpRequest, quiz_url: str):
    quiz_id_str, *_other_url_parts = quiz_url.split('-')
    quiz = None

    try:
        quiz_id = int(quiz_id_str)
    except ValueError:
        raise Http404("Invalid quiz URL")

    quiz = get_object_or_404(Quiz, id=quiz_id)

    if quiz_url != quiz.url:
        return redirect('quiz-page', quiz_url=quiz.url)

    return render(request, 'quiz/quiz.html', {
        'quiz': quiz
    })
