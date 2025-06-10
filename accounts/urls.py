from django.urls import path
from . import views

urlpatterns = [
      path("signup/", views.signup, name = "signup"),
      #127.0.0.1:8000/accounts/signup/
]