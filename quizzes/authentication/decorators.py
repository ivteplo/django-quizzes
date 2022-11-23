# Copyright (c) 2022 Ivan Teplov

from urllib.parse import urlencode
from django.http import HttpRequest
from django.shortcuts import redirect
from django.urls import reverse


def signed_in_only(http_request_handler):
    def resulting_handler(request: HttpRequest, *args, **kwargs):
        if not request.user.is_authenticated:
            # get the path to the sign-in view
            url = reverse(viewname='sign-in')

            # the user should be redirected here after signing in
            url += '?' + urlencode({
                'redirect_to': request.get_full_path()
            })

            # redirect the user
            return redirect(to=url)

        # the user is signed in, so just render the view
        return http_request_handler(request, *args, **kwargs)

    return resulting_handler


def not_signed_in_only(http_request_handler):
    def resulting_handler(request: HttpRequest, *args, **kwargs):
        if request.user.is_authenticated:
            # redirect the user to the home page
            return redirect(to='home')

        # the user is not signed in, so just render the view
        return http_request_handler(request, *args, **kwargs)

    return resulting_handler
