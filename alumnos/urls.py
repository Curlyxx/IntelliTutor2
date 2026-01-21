from django.urls import path
from . import views

app_name = 'alumnos'

urlpatterns = [
    path('', views.alumnos, name='alumnos'),
    
]