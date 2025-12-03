from django.urls import path
from . import views

app_name = 'login'

urlpatterns = [
    path('', views.login_view, name='login_view'),  # Cambiado a login_view
    path('register/', views.register, name='register'),
    path('logout/', views.logout_view, name='logout'),

]