from django.conf import settings
from django.conf.urls.i18n import i18n_patterns
from django.contrib import admin
from django.urls import path, include

# Non-translatable URLs (no language prefix)
urlpatterns = [
    path("admin/", admin.site.urls),
    path("athm/", include("django_athm.urls", namespace="django_athm")),
]

# Translatable URLs (with language prefix: /en/, /es/)
urlpatterns += i18n_patterns(
    path("", include("athm_tip.core.urls")),
    prefix_default_language=True,  # Force /en/ for English
)

if settings.DEBUG:
    # Include django_browser_reload URLs only in DEBUG mode
    urlpatterns += [
        path("__reload__/", include("django_browser_reload.urls")),
    ]
