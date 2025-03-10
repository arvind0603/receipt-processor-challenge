from django.urls import path
from . import views

urlpatterns = [
    path("process", views.process, name="process"),
    path("<uuid:id>/points", views.points, name="points"),
]