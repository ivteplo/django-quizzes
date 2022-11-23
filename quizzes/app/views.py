# Copyright (c) 2022 Ivan Teplov

from quizzes.authentication.decorators import signed_in_only, not_signed_in_only

from django.contrib.auth import authenticate, login, logout, get_user_model
from django.core.exceptions import ValidationError
from django.http import HttpRequest, Http404
from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse

from .helpers import parse_dict_keys, normalize_redirect_to
from .models import Answer, Question, Quiz


User = get_user_model()


def home(request: HttpRequest):
    latest_quizzes = Quiz.objects.all().order_by('-id')[:10]

    return render(request, 'app/index.html', {
        'latest_quizzes': latest_quizzes
    })


def search(request: HttpRequest):
    query = request.GET.get('query', '')
    quizzes = None
    users = None

    if query:
        quizzes = Quiz.objects.filter(name__icontains=query)
        users = User.objects.filter(name__icontains=query)

    return render(request, 'app/search.html', {
        'query': query,
        'quizzes': quizzes,
        'users': users
    })


def profile(request: HttpRequest):
    return render(request, 'app/profile.html')


@signed_in_only
def new_quiz(request: HttpRequest):
    options = {}

    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')

        try:
            quiz = Quiz.objects.create(
                creator=request.user, name=name, description=description)
        except ValidationError as error:
            options['error'] = error
        else:
            return redirect('quiz-page', quiz_url=quiz.id)

    return render(request, 'quiz/new.html', options)


def _get_quiz_by_url(quiz_url: str) -> Quiz or Http404:
    quiz_id_str, *_other_url_parts = quiz_url.split('-')

    try:
        quiz_id = int(quiz_id_str)
    except ValueError:
        raise Http404("Invalid quiz URL")

    quiz = get_object_or_404(Quiz, id=quiz_id)
    return quiz


def quiz_page(request: HttpRequest, quiz_url: str):
    quiz = _get_quiz_by_url(quiz_url)

    if quiz_url != quiz.url:
        return redirect('quiz-page', quiz_url=quiz.url)

    return render(request, 'quiz/quiz.html', {
        'quiz': quiz
    })


@signed_in_only
def edit_quiz(request: HttpRequest, quiz_url: str):
    quiz = _get_quiz_by_url(quiz_url)
    options = {
        'quiz': quiz,
        'error': None
    }

    if quiz_url != quiz.url:
        return redirect('edit-quiz', quiz_url=quiz.url)

    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')

        try:
            quiz.name = name
            quiz.description = description
            quiz.full_clean()
            quiz.save()
        except ValidationError as error:
            options['error'] = error.messages[0]
        else:
            return redirect('quiz-page', quiz_url=quiz.url)

    return render(request, 'quiz/edit.html', options,
                  status=200 if not options['error'] else 400)


def add_quiz_question(request: HttpRequest, quiz_url: str):
    quiz = _get_quiz_by_url(quiz_url)

    if quiz_url != quiz.url:
        return redirect('add-quiz-question', quiz_url=quiz.url)

    if quiz.creator != request.user:
        return redirect('quiz-page', quiz_url=quiz.url)

    question_prompt, question_type, answers = None, None, []
    error = None

    if request.method == 'POST':
        question_prompt = request.POST.get('question')
        question_type_string = request.POST.get('question-type')

        try:
            answers = list(parse_dict_keys(request.POST)['answers'].values())
        except Exception:
            error = 'Answers are specified in a wrong way'
        else:
            if not question_prompt:
                error = 'Please, specify a question'
            elif not question_type_string:
                error = 'Please, choose a question type'
            elif len(answers) == 1:
                error = 'Please, specify more answers'
            else:
                try:
                    question_type = int(question_type_string)
                except ValueError:
                    error = 'Invalid question type'
                else:
                    question = Question.objects.create(
                        quiz=quiz,
                        text=question_prompt,
                        question_type=question_type
                    )

                    for answer in answers:
                        Answer.objects.create(
                            question=question,
                            text=answer['text'],
                            is_right=answer['is_right'] == 'on'
                        )

                    return redirect(to='quiz-page', quiz_url=quiz.url)

    return render(request, 'quiz/add-question.html', {
        'quiz': quiz,
        'question_types': [
            {'id': id, 'text': text}
            for id, text in Question.QUESTION_TYPE_CHOICES
        ],
        'form': {
            'question': question_prompt,
            'question_type': question_type,
            'answers': answers
        },
        'error': error
    }, status=200 if not error else 400)


@not_signed_in_only
def register(request: HttpRequest):
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
                url = normalize_redirect_to(
                    request.GET.get('redirect_to'),
                    reverse('home')
                )

                return redirect(to=url)

    status = 400 if 'error' in options else 200
    return render(request, 'auth/register.html', options, status=status)


@not_signed_in_only
def sign_in(request: HttpRequest):
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
                url = normalize_redirect_to(
                    request.GET.get('redirect_to'),
                    reverse('home')
                )

                return redirect(to=url)

    status = 400 if 'error' in options else 200
    return render(request, 'auth/sign-in.html', options, status=status)


def sign_out(request: HttpRequest):
    if request.user.is_authenticated:
        logout(request)

    return redirect('home')
