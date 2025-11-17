from django.urls import path

from . import views

app_name = "core"

urlpatterns = [
    path("", views.tip_page, name="landing"),
    path("update-athm-button/", views.update_athm_button, name="update_athm_button"),
]
