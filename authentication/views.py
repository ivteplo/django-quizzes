# Copyright (c) 2022 Ivan Teplov

from django.contrib.auth import authenticate, login, logout, get_user_model
from django.core.exceptions import ValidationError
from django.http import HttpRequest
from django.shortcuts import redirect, render
from django.urls import reverse

from .helpers import normalize_redirect_to

from .decorators import not_signed_in_only


User = get_user_model()


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
