# Copyright (c) 2022 Ivan Teplov

from django.urls import reverse


def normalize_redirect_to(url: str or None, default_value: str) -> str:
    if url is None:
        return default_value

    if (
        not url.startswith('/')
        or url.startswith('//')
        or url == reverse('sign-out').rstrip('/')
    ):
        url = default_value

    return url
