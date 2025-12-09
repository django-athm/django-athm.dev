from django.urls import path

from . import views

app_name = "core"

urlpatterns = [
    path("", views.tip_page, name="tip"),
    path("thank-you/", views.thank_you, name="thank_you"),
]
