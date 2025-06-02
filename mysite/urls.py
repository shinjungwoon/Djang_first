#앱연결
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls), # 127.0.0.1:8000/admin/
    path("polls/", include("polls.urls")),
    # 127.0.0.1:8000
]
