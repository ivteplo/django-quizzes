# Copyright (c) 2022 Ivan Teplov

from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('auth/register', views.register, name='register'),
    path('auth/sign-in', views.sign_in, name='sign-in'),
    path('auth/sign-out', views.sign_out, name='sign-out')
]
