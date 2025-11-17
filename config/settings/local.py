"""
Local development settings.
"""

import os
import socket


from .base import *  # noqa: F403

# GENERAL
DEBUG = True

SECRET_KEY = os.getenv("DJANGO_SECRET_KEY", "django-insecure-local-dev-key-change-me")


# https://docs.djangoproject.com/en/dev/ref/settings/#allowed-hosts
ALLOWED_HOSTS = [
    "localhost",
    "0.0.0.0",
    "127.0.0.1",
]

# CACHES
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
        "LOCATION": "",
    }
}

# EMAIL
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"


# django-browser-reload
INSTALLED_APPS += ["django_browser_reload"]  # noqa F405
MIDDLEWARE += ["django_browser_reload.middleware.BrowserReloadMiddleware"]  # noqa F405

INTERNAL_IPS = [
    "127.0.0.1",
]

# Showing the debug toolbar when using Docker
hostname, _, ips = socket.gethostbyname_ex(socket.gethostname())
INTERNAL_IPS += [ip[:-1] + "1" for ip in ips]
