import os

import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

from .base import *  # noqa

ALLOWED_HOSTS = [
    "localhost",  # for coolify health checks
    "django-athm.dev",
]

IS_PRODUCTION = True

# SECURITY
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

SECURE_SSL_REDIRECT = True

SESSION_COOKIE_SECURE = True

X_FRAME_OPTIONS = "DENY"

CSRF_COOKIE_SECURE = True

SECURE_HSTS_SECONDS = 60

SECURE_BROWSER_XSS_FILTER = True

SECURE_CONTENT_TYPE_NOSNIFF = True

# sentry
SENTRY_DSN = os.getenv("SENTRY_DSN")

if SENTRY_DSN:
    sentry_sdk.init(
        dsn=SENTRY_DSN,
        integrations=[
            DjangoIntegration(),
        ],
    )
# LOGGING
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "%(levelname)s %(asctime)s %(module)s "
            "%(process)d %(thread)d %(message)s"
        }
    },
    "handlers": {
        "console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "verbose",
        }
    },
    "root": {"level": "INFO", "handlers": ["console"]},
    "loggers": {
        "django.db.backends": {
            "level": "ERROR",
            "handlers": ["console"],
            "propagate": False,
        },
        "django.security.DisallowedHost": {
            "level": "ERROR",
            "handlers": ["console"],
            "propagate": False,
        },
        "django_athm": {
            "level": "INFO",
            "handlers": ["console"],
            "propagate": False,
        },
    },
}


# Admin notifications (receives transaction alerts)
ADMINS = [("Admin", os.getenv("ADMIN_EMAIL", "admin@localhost"))]

# django-anymail (Amazon SES)
EMAIL_BACKEND = "anymail.backends.amazon_ses.EmailBackend"
DEFAULT_FROM_EMAIL = os.getenv("DEFAULT_FROM_EMAIL", "noreply@localhost")
SERVER_EMAIL = os.getenv("SERVER_EMAIL", "noreply@localhost")

ANYMAIL = {
    "AMAZON_SES_CLIENT_PARAMS": {
        "region_name": os.getenv("AWS_SES_REGION_NAME", "us-east-1"),
    },
}
