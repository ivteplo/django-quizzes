# Copyright (c) 2022 Ivan Teplov

from django.urls import path
from . import views


urlpatterns = [
    path('register', views.register, name='register'),
    path('sign-in', views.sign_in, name='sign-in'),
    path('sign-out', views.sign_out, name='sign-out')
]
