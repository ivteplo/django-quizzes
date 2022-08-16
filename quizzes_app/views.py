# Copyright (c) 2022 Ivan Teplov

from django.contrib.auth import authenticate, login, logout
from django.core.exceptions import ValidationError
from django.http import HttpRequest, Http404
from django.shortcuts import redirect, render, get_object_or_404

from .models import User, Quiz

# TODO: create decorators for signed_in_only and not_signed_in_only


def index(request: HttpRequest):
    return render(request, 'app/index.html')


def register(request: HttpRequest):
    if request.user.is_authenticated:
        return redirect(to='index')

    options = {}

    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        repeated_password = request.POST.get('repeated-password')

        if not name:
            options['error'] = 'Please, specify your name'
        elif not email:
            options['error'] = 'Please, specify your email'
        elif not password:
            options['error'] = 'Please, specify a password'
        elif not repeated_password:
            options['error'] = 'Please, repeat your password'
        elif repeated_password != password:
            options['error'] = "Passwords don't match"
        else:
            try:
                user = User.objects.create_user(
                    name=name,
                    email=email,
                    password=password
                )

                login(request, user)
            except ValidationError as error:
                options['error'] = error.message
            else:
                return redirect(to='index')


    return render(request, 'auth/register.html', options)


def sign_in(request: HttpRequest):
    if request.user.is_authenticated:
        return redirect(to='index')

    options = {}

    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        if not email:
            options['error'] = 'Please, specify your email'
        elif not password:
            options['error'] = 'Please, specify a password'
        else:
            try:
                user = authenticate(request, email=email, password=password)

                if user:
                    login(request, user)
                else:
                    raise ValidationError('Invalid email or password')
            except ValidationError as error:
                options['error'] = error.message
            else:
                return redirect(to='index')


    return render(request, 'auth/sign-in.html', options)


def sign_out(request: HttpRequest):
    if request.user.is_authenticated:
        logout(request)

    return redirect('index')


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
    quiz_id_str, *other_url_parts = quiz_url.split('-')
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
