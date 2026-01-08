from django.shortcuts import render, redirect, get_object_or_404
from django.db import connection
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from functools import wraps
import json
import re
from datetime import datetime, date

def require_profesor(view_func):
    """
    Decorador que verifica si el usuario logueado es profesor
    """
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        # Verificar si hay sesión activa
        if not request.session.get('user_id'):
            return redirect('login:login_view')
        
        # Verificar si el rol es profesor
        user_role = request.session.get('user_role')
        if user_role != 'profesor':
            return JsonResponse({'success': False, 'message': 'Acceso denegado. Solo profesores.'}) if request.headers.get('Content-Type') == 'application/json' else redirect('login:login_view')
        
        return view_func(request, *args, **kwargs)
    return wrapper

@require_profesor
def portal_profesor(request):
    # Obtener el username de la sesión
    username = request.session.get('username', 'profesor')
    
    context = {
        'user_name': username,
    }
    return render(request, 'profesores/profesores.html', context)

@require_profesor
def mis_grupos(request):
    """
    Vista para mostrar los grupos del profesor basados en el período actual
    """
    # Obtener el ID del profesor de la sesión
    profesor_id = request.session.get('user_id')
    username = request.session.get('username', 'profesor')
    
    # Obtener la fecha actual
    hoy = date.today()
    
    with connection.cursor() as cursor:
        try:
            # Primero, verificar que el profesor existe en la tabla usuarios
            cursor.execute("SELECT id FROM usuarios WHERE id = %s AND rol = 'profesor'", [profesor_id])
            if not cursor.fetchone():
                messages.error(request, 'No se encontró información del profesor.')
                return redirect('profesores:portal_profesor')
            
            # Obtener el semestre activo (que incluye la fecha actual)
            cursor.execute("""
                SELECT id, nombre, fecha_inicio, fecha_fin, activo 
                FROM semestres 
                WHERE activo = 1 
                ORDER BY fecha_fin DESC 
                LIMIT 1
            """)
            
            semestre_result = cursor.fetchone()
            
            if semestre_result:
                semestre_id, semestre_nombre, fecha_inicio, fecha_fin, activo = semestre_result
                periodo_actual = {
                    'id': semestre_id,
                    'nombre': semestre_nombre,
                    'fecha_inicio': fecha_inicio,
                    'fecha_fin': fecha_fin,
                    'activo': activo
                }
            else:
                periodo_actual = None
                semestre_id = None
            
            # Obtener grupos del profesor - Consulta mejorada
            query = """
                SELECT 
                    g.id,
                    g.nombre,
                    g.descripcion,
                    g.turno,
                    g.fecha_inicio,
                    g.fecha_fin,
                    g.activo,
                    DATE_FORMAT(g.fecha_creacion, '%%d/%%m/%%Y') as fecha_creacion,
                    g.evaluacion_finalizada,
                    m.nombre as materia_nombre,
                    m.id as materia_id,
                    s.nombre as semestre_nombre,
                    s.id as semestre_id
                FROM grupos g
                INNER JOIN materias m ON g.materia_id = m.id
                INNER JOIN semestres s ON g.semestre_id = s.id
                WHERE g.profesor_id = %s
            """
            
            params = [profesor_id]
            
            # Si hay período actual, filtrar por él
            if periodo_actual and semestre_id:
                query += " AND g.semestre_id = %s"
                params.append(semestre_id)
            
            query += " ORDER BY g.activo DESC, g.turno, g.nombre"
            
            cursor.execute(query, params)
            columns = [col[0] for col in cursor.description]
            grupos_data = [dict(zip(columns, row)) for row in cursor.fetchall()]
            
            # Si no hay grupos, mostrar todos sin filtrar por semestre
            if not grupos_data and periodo_actual and semestre_id:
                cursor.execute("""
                    SELECT 
                        g.id,
                        g.nombre,
                        g.descripcion,
                        g.turno,
                        g.fecha_inicio,
                        g.fecha_fin,
                        g.activo,
                        DATE_FORMAT(g.fecha_creacion, '%%d/%%m/%%Y') as fecha_creacion,
                        g.evaluacion_finalizada,
                        m.nombre as materia_nombre,
                        m.id as materia_id,
                        s.nombre as semestre_nombre,
                        s.id as semestre_id
                    FROM grupos g
                    INNER JOIN materias m ON g.materia_id = m.id
                    INNER JOIN semestres s ON g.semestre_id = s.id
                    WHERE g.profesor_id = %s
                    ORDER BY g.activo DESC, g.turno, g.nombre
                """, [profesor_id])
                
                columns = [col[0] for col in cursor.description]
                grupos_data = [dict(zip(columns, row)) for row in cursor.fetchall()]
            
            # Calcular estadísticas
            total_grupos = len(grupos_data)
            grupos_activos = sum(1 for grupo in grupos_data if grupo['activo'])
            
            # Contar materias diferentes
            materias_ids = set(grupo['materia_id'] for grupo in grupos_data if grupo['materia_id'])
            materias_count = len(materias_ids)
            
            # Contar estudiantes totales - VERIFICAR EL NOMBRE EXACTO DE LA TABLA
            total_estudiantes = 0
            if grupos_data:
                grupo_ids = [grupo['id'] for grupo in grupos_data]
                placeholders = ','.join(['%s'] * len(grupo_ids))
                
                # Intentar con diferentes nombres de tabla
                try:
                    cursor.execute(f"""
                        SELECT COUNT(DISTINCT estudiante_id) 
                        FROM estudiante_grupos 
                        WHERE grupo_id IN ({placeholders})
                    """, grupo_ids)
                except Exception as e:
                    # Si falla, intentar con otro nombre posible
                    try:
                        cursor.execute(f"""
                            SELECT COUNT(DISTINCT estudiante_id) 
                            FROM estudiante_grupo 
                            WHERE grupo_id IN ({placeholders})
                        """, grupo_ids)
                    except Exception:
                        # Si no existe la tabla, simplemente mostrar 0
                        total_estudiantes = 0
                        print(f"Error al buscar tabla de estudiantes: {e}")
                        pass
                
                result = cursor.fetchone()
                total_estudiantes = result[0] if result else 0
                
        except Exception as e:
            print(f"Error en mis_grupos: {str(e)}")  # Para depuración
            messages.error(request, 'Error al cargar los grupos. Contacta al administrador.')
            grupos_data = []
            periodo_actual = None
            total_grupos = 0
            grupos_activos = 0
            materias_count = 0
            total_estudiantes = 0
    
    context = {
        'grupos': grupos_data,
        'periodo_actual': periodo_actual,
        'total_grupos': total_grupos,
        'grupos_activos': grupos_activos,
        'materias_count': materias_count,
        'total_estudiantes': total_estudiantes,
        'user_name': username,
    }
    
    return render(request, 'profesores/menu/grupos.html', context)

@require_profesor
def detalle_grupo(request, grupo_id):
    """
    Vista para mostrar el detalle de un grupo específico
    """
    # Obtener el ID del profesor de la sesión
    profesor_id = request.session.get('user_id')
    username = request.session.get('username', 'profesor')
    
    with connection.cursor() as cursor:
        # Verificar que el grupo pertenece al profesor actual y obtener detalles
        cursor.execute("""
            SELECT 
                g.id,
                g.nombre,
                g.descripcion,
                g.turno,
                g.fecha_inicio,
                g.fecha_fin,
                g.activo,
                g.fecha_creacion,
                g.evaluacion_finalizada,
                m.nombre as materia_nombre,
                m.id as materia_id,
                m.descripcion as materia_descripcion,
                m.creditos as materia_creditos,
                s.nombre as semestre_nombre,
                s.id as semestre_id,
                s.fecha_inicio as semestre_inicio,
                s.fecha_fin as semestre_fin
            FROM grupos g
            LEFT JOIN materias m ON g.materia_id = m.id
            LEFT JOIN semestres s ON g.semestre_id = s.id
            WHERE g.id = %s AND g.profesor_id = %s
        """, [grupo_id, profesor_id])
        
        result = cursor.fetchone()
        
        if not result:
            messages.error(request, 'Grupo no encontrado o no tienes permisos para verlo.')
            return redirect('profesores:mis_grupos')
        
        columns = [col[0] for col in cursor.description]
        grupo = dict(zip(columns, result))
        
        # Obtener estudiantes del grupo
        cursor.execute("""
            SELECT 
                u.id,
                u.nombre,
                u.apellido,
                u.email,
                u.numero_cuenta,
                u.telefono,
                eg.fecha_inscripcion
            FROM estudiante_grupos eg
            LEFT JOIN usuarios u ON eg.estudiante_id = u.id
            WHERE eg.grupo_id = %s
            ORDER BY u.apellido, u.nombre
        """, [grupo_id])
        
        estudiantes_columns = [col[0] for col in cursor.description]
        estudiantes = [dict(zip(estudiantes_columns, row)) for row in cursor.fetchall()]
        
        # Obtener prácticas del grupo
        cursor.execute("""
            SELECT 
                p.id,
                p.nombre,
                p.descripcion,
                p.fecha_inicio,
                p.fecha_fin,
                p.activa,
                COUNT(DISTINCT ep.id) as entregas_totales,
                COUNT(DISTINCT CASE WHEN ep.calificacion IS NOT NULL THEN ep.id END) as entregas_calificadas
            FROM practicas p
            LEFT JOIN entrega_practicas ep ON p.id = ep.practica_id
            WHERE p.grupo_id = %s
            GROUP BY p.id
            ORDER BY p.fecha_inicio DESC
        """, [grupo_id])
        
        practicas_columns = [col[0] for col in cursor.description]
        practicas = [dict(zip(practicas_columns, row)) for row in cursor.fetchall()]
    
    context = {
        'grupo': grupo,
        'estudiantes': estudiantes,
        'practicas': practicas,
        'total_estudiantes': len(estudiantes),
        'total_practicas': len(practicas),
        'user_name': username,
    }
    
    return render(request, 'profesores/menu/detalle_grupo.html', context)

@require_profesor
def crear_practicas(request):
    """
    Vista para crear prácticas (página vacía por ahora)
    """
    username = request.session.get('username', 'profesor')
    
    context = {
        'user_name': username,
    }
    return render(request, 'profesores/menu/crear_practicas.html', context)

@require_profesor
def calificaciones(request):
    """
    Vista para ver calificaciones (página vacía por ahora)
    """
    username = request.session.get('username', 'profesor')
    
    context = {
        'user_name': username,
    }
    return render(request, 'profesores/menu/calificaciones.html', context)

@require_profesor
def reportes(request):
    """
    Vista para ver reportes (página vacía por ahora)
    """
    username = request.session.get('username', 'profesor')
    
    context = {
        'user_name': username,
    }
    return render(request, 'profesores/menu/reportes.html', context)