from django.urls import path

from . import views

app_name = "core"

urlpatterns = [
    path("", views.tip_page, name="tip"),
    path("demo", views.demo_page, name="demo"),
    path("tip/", views.tip_page, name="tip_alt"),
    path("thank-you/<str:reference_number>/", views.thank_you, name="thank_you"),
]
