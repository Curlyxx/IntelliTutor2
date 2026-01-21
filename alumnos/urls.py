from django.urls import path
from . import views

app_name = 'alumnos'

urlpatterns = [
    path('', views.alumnos, name='alumnos'),
    path('editar-perfil/', views.editar_perfil, name='editar_perfil'),
    path('cambiar-password/', views.cambiar_password, name='cambiar_password'),
    path('info-sistema/', views.info_sistema, name='info_sistema'),
    
    # Nuevas rutas para cursos
    path('mis-cursos/', views.mis_cursos, name='mis_cursos'),
    path('curso/<int:curso_id>/', views.detalle_curso, name='detalle_curso'),
    path('cursos-disponibles/', views.cursos_disponibles, name='cursos_disponibles'),
    path('solicitar-inscripcion/<int:grupo_id>/', views.solicitar_inscripcion, name='solicitar_inscripcion'),
    path('abandonar-curso/<int:curso_id>/', views.abandonar_curso, name='abandonar_curso'),
]