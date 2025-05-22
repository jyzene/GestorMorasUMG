# moras/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('buscar/', views.buscar_estudiante, name='buscar_estudiante'),
]
