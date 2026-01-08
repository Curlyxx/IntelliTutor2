from django.urls import path
from . import views

app_name = 'profesores'

urlpatterns = [
    # Portal principal
    path('', views.portal_profesor, name='profesores'),
    
    # Gestión de grupos
    path('mis-grupos/', views.mis_grupos, name='mis_grupos'),
    path('grupo/<int:grupo_id>/', views.detalle_grupo, name='detalle_grupo'),
    
    # Otras secciones (puedes implementarlas después)
    path('crear-practicas/', views.crear_practicas, name='crear_practicas'),
    path('calificaciones/', views.calificaciones, name='calificaciones'),
    path('reportes/', views.reportes, name='reportes'),
]