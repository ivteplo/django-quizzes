# Copyright (c) 2022 Ivan Teplov

from django.shortcuts import render


def index(request):
    return render(request, 'index.html')
