from django.contrib import admin
from django.urls import path
from project import views

urlpatterns = [
    path("", views.index, name="home"),
    path("about", views.about, name="about")
]
