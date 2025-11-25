from django.urls import path

from . import views

app_name = "core"

urlpatterns = [
    path("", views.tip_page, name="tip"),
]
