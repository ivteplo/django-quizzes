# Copyright (c) 2022 Ivan Teplov

from django import template
from django.urls import reverse


register = template.Library()


@register.filter
def reverse_url(url_name, *args, **kwargs):
    return reverse(url_name, args=args, kwargs=kwargs)
