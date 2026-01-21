from django.urls import path
from . import views

app_name = 'administradores'

urlpatterns = [
    # Para ir al admin
    path('', views.admin, name='admin'),
    # Usuarios
    path('usuarios/', views.usuarios, name='usuarios'),
    path('cambiar-rol/', views.cambiar_rol, name='cambiar_rol'),
    path('usuario/<int:user_id>/', views.editar_usuario, name='editar_usuario'),
    path('actualizar-usuario/', views.actualizar_usuario, name='actualizar_usuario'),
    # Materias
    path('materias/', views.materias, name='materias'),
    path('crear-materia/', views.crear_materia, name='crear_materia'),
    path('actualizar-materia/', views.actualizar_materia, name='actualizar_materia'),
    path('eliminar-materia/', views.eliminar_materia, name='eliminar_materia'),
    # Semestres
    path('semestres/', views.semestres, name='semestres'),
    path('crear_semestre/', views.crear_semestre, name='crear_semestre'),
    path('actualizar_semestre/', views.actualizar_semestre, name='actualizar_semestre'),
    path('eliminar_semestre/', views.eliminar_semestre, name='eliminar_semestre'),
    path('toggle_semestre/', views.toggle_semestre, name='toggle_semestre'),
    # Grupos
    path('grupos/', views.grupos, name='grupos'),
    path('crear_grupo/', views.crear_grupo, name='crear_grupo'),
    path('actualizar_grupo/', views.actualizar_grupo, name='actualizar_grupo'),
    path('eliminar_grupo/', views.eliminar_grupo, name='eliminar_grupo'),
    path('toggle_grupo/', views.toggle_grupo, name='toggle_grupo'),
    
    # Sección del botón de Perfil del admin
    path('perfil/', views.perfil_usuario, name='perfil_usuario'),
    path('actualizar-perfil/', views.actualizar_perfil, name='actualizar_perfil'),
    path('cambiar-password/', views.cambiar_password, name='cambiar_password'),
    path('cerrar-sesion/', views.cerrar_sesion, name='cerrar_sesion'),
    path('subir-avatar/', views.subir_avatar, name='subir_avatar'),
]