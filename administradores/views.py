from django.shortcuts import render, redirect
from django.db import connection
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from functools import wraps
import json
import re
from datetime import datetime, date
from django.contrib.auth import logout as auth_logout
import hashlib
from django.contrib import messages

def require_admin(view_func):
    """
    Decorador que verifica si el usuario logueado es administrador
    """
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        # Verificar si hay sesión activa
        if not request.session.get('user_id'):
            return redirect('login:login_view')
        
        # Verificar si el rol es administrador
        user_role = request.session.get('user_role')
        
        if user_role != 'administrador':
            return JsonResponse({'success': False, 'message': 'Acceso denegado. Solo administradores.'}) if request.headers.get('Content-Type') == 'application/json' else redirect('login:login_view')
        
        return view_func(request, *args, **kwargs)
    return wrapper


def cerrar_sesion(request):
    """
    Vista para cerrar sesión
    """
    # Limpiar la sesión
    request.session.flush()
    
    # Redirigir al login
    return redirect('login:login_view')


@require_admin
def admin(request):
    # Obtener el username de la sesión
    username = request.session.get('username', 'admin')
    
    context = {
        'user_name': username,  # Ahora user_name será el username
    }
    return render(request, 'admin/admin.html', context)

@require_admin
def usuarios(request):
    # Obtener el username de la sesión
    username = request.session.get('username', 'admin')
    
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT id, nombre, apellido, email, rol, fecha_creacion, numero_cuenta, telefono, usuario
            FROM usuarios 
            ORDER BY 
                CASE rol 
                    WHEN 'administrador' THEN 1
                    WHEN 'profesor' THEN 2
                    WHEN 'estudiante' THEN 3
                    ELSE 4
                END,
                nombre ASC
        """)
        
        columns = [col[0] for col in cursor.description]
        usuarios_data = []
        
        for row in cursor.fetchall():
            usuario_dict = dict(zip(columns, row))
            usuarios_data.append(usuario_dict)
    
    context = {
        'usuarios': usuarios_data,
        'user_name': username,  # Usar el username, no el nombre completo
    }
    return render(request, 'admin/menu/usuarios.html', context)

@require_admin
@csrf_exempt
def cambiar_rol(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            user_id = data.get('user_id')
            new_role = data.get('new_role')
            
            # Validar que el rol sea válido
            if new_role not in ['administrador', 'profesor', 'estudiante']:
                return JsonResponse({'success': False, 'message': 'Rol inválido'})
            
            # Verificar que el usuario actual es administrador y obtener info del usuario a cambiar
            current_admin_id = request.session.get('user_id')
            
            with connection.cursor() as cursor:
                cursor.execute("SELECT rol FROM usuarios WHERE id = %s", [user_id])
                result = cursor.fetchone()
                
                if not result:
                    return JsonResponse({'success': False, 'message': 'Usuario no encontrado'})
                
                current_role = result[0]
                
                # Verificar si es el mismo rol
                if current_role == new_role:
                    return JsonResponse({'success': False, 'message': 'El rol seleccionado es el mismo que el actual'})
                
                # Actualizar el rol
                cursor.execute("UPDATE usuarios SET rol = %s WHERE id = %s", [new_role, user_id])
                
                return JsonResponse({
                    'success': True, 
                    'message': f'Rol cambiado exitosamente de "{current_role}" a "{new_role}"'
                })
                
        except Exception as e:
            return JsonResponse({'success': False, 'message': f'Error: {str(e)}'})
    
    return JsonResponse({'success': False, 'message': 'Método no permitido'})

@require_admin
def editar_usuario(request, user_id):
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT id, nombre, apellido, email, rol, fecha_creacion, numero_cuenta, telefono, usuario
            FROM usuarios 
            WHERE id = %s
        """, [user_id])
        
        result = cursor.fetchone()
        if not result:
            return redirect('administradores:usuarios')
        
        columns = [col[0] for col in cursor.description]
        usuario = dict(zip(columns, result))
    
    return render(request, 'admin/menu/editar_usuario.html', {'usuario': usuario})

@require_admin
@csrf_exempt
def actualizar_usuario(request):
    if request.method == 'POST':
        try:
            import re
            data = json.loads(request.body)
            user_id = data.get('user_id')
            nombre = data.get('nombre', '').strip()
            apellido = data.get('apellido', '').strip()
            usuario = data.get('usuario', '').strip()
            email = data.get('email', '').strip()
            telefono = data.get('telefono', '').strip()
            
            # Validaciones
            if not all([nombre, apellido, usuario, email, telefono]):
                return JsonResponse({'success': False, 'message': 'Todos los campos son obligatorios'})
            
            # Validar formato de nombre y apellido
            if not re.match(r'^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s]+$', nombre) or len(nombre) > 100:
                return JsonResponse({'success': False, 'message': 'Nombre inválido: solo letras, acentos, ñ y espacios (máx. 100 caracteres)'})
            
            if not re.match(r'^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s]+$', apellido) or len(apellido) > 70:
                return JsonResponse({'success': False, 'message': 'Apellido inválido: solo letras, acentos, ñ y espacios (máx. 70 caracteres)'})
            
            # Validar usuario
            if len(usuario) > 50:
                return JsonResponse({'success': False, 'message': 'Usuario muy largo (máx. 50 caracteres)'})
            
            # Validar email
            if not re.match(r'^[^\s@]+@[^\s@]+\.[^\s@]+$', email):
                return JsonResponse({'success': False, 'message': 'Formato de correo inválido'})
            
            # Validar teléfono (obligatorio)
            if not re.match(r'^[0-9]{10}$', telefono):
                return JsonResponse({'success': False, 'message': 'Teléfono inválido: exactamente 10 dígitos'})
            
            with connection.cursor() as cursor:
                # Verificar que el usuario existe
                cursor.execute("SELECT id FROM usuarios WHERE id = %s", [user_id])
                if not cursor.fetchone():
                    return JsonResponse({'success': False, 'message': 'Usuario no encontrado'})
                
                # Verificar que el email y usuario no estén en uso por otro usuario
                cursor.execute("""
                    SELECT id FROM usuarios 
                    WHERE (email = %s OR usuario = %s) AND id != %s
                """, [email, usuario, user_id])
                
                if cursor.fetchone():
                    return JsonResponse({'success': False, 'message': 'El correo electrónico o nombre de usuario ya está en uso por otro usuario'})
                
                # Actualizar usuario
                cursor.execute("""
                    UPDATE usuarios 
                    SET nombre = %s, apellido = %s, usuario = %s, email = %s, telefono = %s
                    WHERE id = %s
                """, [nombre, apellido, usuario, email, telefono, user_id])
                
                return JsonResponse({
                    'success': True, 
                    'message': 'Usuario actualizado exitosamente'
                })
                
        except Exception as e:
            return JsonResponse({'success': False, 'message': f'Error al actualizar usuario: {str(e)}'})
    
    return JsonResponse({'success': False, 'message': 'Método no permitido'})

@require_admin
def materias(request):
    # Obtener el username de la sesión
    username = request.session.get('username', 'admin')  # <- Agrega esta línea
    
    with connection.cursor() as cursor:
        cursor.execute("SELECT id, nombre, descripcion, creditos FROM materias ORDER BY nombre ASC")
        columns = [col[0] for col in cursor.description]
        materias_data = []
        
        for row in cursor.fetchall():
            materia_dict = dict(zip(columns, row))
            materias_data.append(materia_dict)
    
    # Pasar username en el contexto
    return render(request, 'admin/menu/materias.html', {
        'materias': materias_data,
        'user_name': username  # <- Agrega esto
    })

@require_admin
@csrf_exempt
def crear_materia(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            nombre = data.get('nombre', '').strip()
            descripcion = data.get('descripcion', '').strip()
            creditos = data.get('creditos')  # Ya es un número, no usar .strip()
            
            if not nombre or creditos is None:
                return JsonResponse({'success': False, 'message': 'Nombre y créditos son obligatorios'})
            
            # Verificar que créditos sea un número válido
            try:
                creditos = int(creditos)
                if creditos <= 0:
                    return JsonResponse({'success': False, 'message': 'Los créditos deben ser un número positivo'})
            except (ValueError, TypeError):
                return JsonResponse({'success': False, 'message': 'Los créditos deben ser un número válido'})
            
            with connection.cursor() as cursor:
                cursor.execute("SELECT id FROM materias WHERE nombre = %s", [nombre])
                if cursor.fetchone():
                    return JsonResponse({'success': False, 'message': 'Ya existe una materia con ese nombre'})
                
                cursor.execute(
                    "INSERT INTO materias (nombre, descripcion, creditos) VALUES (%s, %s, %s)",
                    [nombre, descripcion if descripcion else None, creditos]
                )
                
                return JsonResponse({'success': True, 'message': 'Materia creada exitosamente'})
                
        except Exception as e:
            return JsonResponse({'success': False, 'message': f'Error al crear materia: {str(e)}'})
    
    return JsonResponse({'success': False, 'message': 'Método no permitido'})

@require_admin
@csrf_exempt
def actualizar_materia(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            materia_id = data.get('materia_id')
            nombre = data.get('nombre', '').strip()
            descripcion = data.get('descripcion', '').strip()
            creditos = data.get('creditos')  # Cambiar: no usar .strip() porque es número
            
            if not nombre or creditos is None:  # Cambiar esta validación
                return JsonResponse({'success': False, 'message': 'Nombre y créditos son obligatorios'})
            
            # Verificar que créditos sea un número válido
            try:
                creditos = int(creditos)
                if creditos <= 0:
                    return JsonResponse({'success': False, 'message': 'Los créditos deben ser un número positivo'})
            except (ValueError, TypeError):
                return JsonResponse({'success': False, 'message': 'Los créditos deben ser un número válido'})
            
            with connection.cursor() as cursor:
                cursor.execute("SELECT id FROM materias WHERE nombre = %s AND id != %s", [nombre, materia_id])
                if cursor.fetchone():
                    return JsonResponse({'success': False, 'message': 'Ya existe otra materia con ese nombre'})
                
                cursor.execute(
                    "UPDATE materias SET nombre = %s, descripcion = %s, creditos = %s WHERE id = %s",
                    [nombre, descripcion if descripcion else None, creditos, materia_id]
                )
                
                return JsonResponse({'success': True, 'message': 'Materia actualizada exitosamente'})
                
        except Exception as e:
            return JsonResponse({'success': False, 'message': f'Error al actualizar materia: {str(e)}'})
    
    return JsonResponse({'success': False, 'message': 'Método no permitido'})

@require_admin
@csrf_exempt
def eliminar_materia(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            materia_id = data.get('materia_id')
            
            with connection.cursor() as cursor:
                cursor.execute("SELECT nombre FROM materias WHERE id = %s", [materia_id])
                result = cursor.fetchone()
                
                if not result:
                    return JsonResponse({'success': False, 'message': 'Materia no encontrada'})
                
                cursor.execute("DELETE FROM materias WHERE id = %s", [materia_id])
                
                return JsonResponse({'success': True, 'message': 'Materia eliminada exitosamente'})
                
        except Exception as e:
            return JsonResponse({'success': False, 'message': f'Error al eliminar materia: {str(e)}'})
    
    return JsonResponse({'success': False, 'message': 'Método no permitido'})


@require_admin
@csrf_exempt
def crear_semestre(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            nombre = data.get('nombre', '').strip()
            fecha_inicio = data.get('fecha_inicio')
            fecha_fin = data.get('fecha_fin')
            activo = data.get('activo', False)
            
            # Validaciones
            if not all([nombre, fecha_inicio, fecha_fin]):
                return JsonResponse({'success': False, 'message': 'Todos los campos son obligatorios'})
            
            # Validar fechas
            try:
                fecha_inicio_dt = datetime.strptime(fecha_inicio, '%Y-%m-%d').date()
                fecha_fin_dt = datetime.strptime(fecha_fin, '%Y-%m-%d').date()
                
                if fecha_inicio_dt >= fecha_fin_dt:
                    return JsonResponse({'success': False, 'message': 'La fecha de fin debe ser posterior a la fecha de inicio'})
                
                # REMOVER esta validación para permitir crear semestres con fechas pasadas
                # if fecha_inicio_dt < date.today():
                #     return JsonResponse({'success': False, 'message': 'La fecha de inicio no puede ser en el pasado'})
                    
            except ValueError:
                return JsonResponse({'success': False, 'message': 'Formato de fecha inválido'})
            
            with connection.cursor() as cursor:
                # Verificar si ya existe un semestre con ese nombre
                cursor.execute("SELECT id FROM semestres WHERE nombre = %s", [nombre])
                if cursor.fetchone():
                    return JsonResponse({'success': False, 'message': 'Ya existe un semestre con ese nombre'})
                
                # Si se va a activar, desactivar todos los demás
                if activo:
                    cursor.execute("UPDATE semestres SET activo = 0")
                
                # Insertar nuevo semestre
                cursor.execute(
                    "INSERT INTO semestres (nombre, fecha_inicio, fecha_fin, activo) VALUES (%s, %s, %s, %s)",
                    [nombre, fecha_inicio_dt, fecha_fin_dt, 1 if activo else 0]
                )
                
                return JsonResponse({'success': True, 'message': 'Semestre creado exitosamente'})
                
        except Exception as e:
            return JsonResponse({'success': False, 'message': f'Error al crear semestre: {str(e)}'})
    
    return JsonResponse({'success': False, 'message': 'Método no permitido'})

@require_admin
@csrf_exempt
def actualizar_semestre(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            semestre_id = data.get('semestre_id')
            nombre = data.get('nombre', '').strip()
            fecha_inicio = data.get('fecha_inicio')
            fecha_fin = data.get('fecha_fin')
            activo = data.get('activo', False)
            
            if not all([nombre, fecha_inicio, fecha_fin]):
                return JsonResponse({'success': False, 'message': 'Todos los campos son obligatorios'})
            
            try:
                fecha_inicio_dt = datetime.strptime(fecha_inicio, '%Y-%m-%d').date()
                fecha_fin_dt = datetime.strptime(fecha_fin, '%Y-%m-%d').date()
                
                if fecha_inicio_dt >= fecha_fin_dt:
                    return JsonResponse({'success': False, 'message': 'La fecha de fin debe ser posterior a la fecha de inicio'})
                
                # REMOVER esta validación para permitir editar semestres con fechas pasadas
                # if fecha_inicio_dt < date.today():
                #     return JsonResponse({'success': False, 'message': 'La fecha de inicio no puede ser en el pasado'})
                    
            except ValueError:
                return JsonResponse({'success': False, 'message': 'Formato de fecha inválido'})
            
            with connection.cursor() as cursor:
                # Verificar si ya existe otro semestre con ese nombre
                cursor.execute("SELECT id FROM semestres WHERE nombre = %s AND id != %s", [nombre, semestre_id])
                if cursor.fetchone():
                    return JsonResponse({'success': False, 'message': 'Ya existe otro semestre con ese nombre'})
                
                # Si se va a activar, desactivar todos los demás
                if activo:
                    cursor.execute("UPDATE semestres SET activo = 0")
                
                # Actualizar semestre
                cursor.execute(
                    "UPDATE semestres SET nombre = %s, fecha_inicio = %s, fecha_fin = %s, activo = %s WHERE id = %s",
                    [nombre, fecha_inicio_dt, fecha_fin_dt, 1 if activo else 0, semestre_id]
                )
                
                return JsonResponse({'success': True, 'message': 'Semestre actualizado exitosamente'})
                
        except Exception as e:
            return JsonResponse({'success': False, 'message': f'Error al actualizar semestre: {str(e)}'})
    
    return JsonResponse({'success': False, 'message': 'Método no permitido'})

@require_admin
@csrf_exempt
def eliminar_semestre(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            semestre_id = data.get('semestre_id')
            
            with connection.cursor() as cursor:
                # Verificar que el semestre existe
                cursor.execute("SELECT nombre FROM semestres WHERE id = %s", [semestre_id])
                result = cursor.fetchone()
                
                if not result:
                    return JsonResponse({'success': False, 'message': 'Semestre no encontrado'})
                
                # Verificar si hay grupos asociados al semestre
                cursor.execute("SELECT COUNT(*) FROM grupos WHERE semestre_id = %s", [semestre_id])
                grupos_count = cursor.fetchone()[0]
                
                if grupos_count > 0:
                    return JsonResponse({'success': False, 'message': f'No se puede eliminar el semestre porque tiene {grupos_count} grupos asociados'})
                
                # Eliminar semestre
                cursor.execute("DELETE FROM semestres WHERE id = %s", [semestre_id])
                
                return JsonResponse({'success': True, 'message': 'Semestre eliminado exitosamente'})
                
        except Exception as e:
            return JsonResponse({'success': False, 'message': f'Error al eliminar semestre: {str(e)}'})
    
    return JsonResponse({'success': False, 'message': 'Método no permitido'})

@require_admin
@csrf_exempt
def toggle_semestre(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            semestre_id = data.get('semestre_id')
            
            with connection.cursor() as cursor:
                # Obtener estado actual
                cursor.execute("SELECT activo FROM semestres WHERE id = %s", [semestre_id])
                result = cursor.fetchone()
                
                if not result:
                    return JsonResponse({'success': False, 'message': 'Semestre no encontrado'})
                
                nuevo_estado = 0 if result[0] == 1 else 1
                
                # Si se va a activar, desactivar todos los demás
                if nuevo_estado == 1:
                    cursor.execute("UPDATE semestres SET activo = 0")
                
                # Actualizar estado del semestre
                cursor.execute("UPDATE semestres SET activo = %s WHERE id = %s", [nuevo_estado, semestre_id])
                
                estado_texto = "activado" if nuevo_estado == 1 else "desactivado"
                return JsonResponse({'success': True, 'message': f'Semestre {estado_texto} exitosamente'})
                
        except Exception as e:
            return JsonResponse({'success': False, 'message': f'Error al cambiar estado del semestre: {str(e)}'})
    
    return JsonResponse({'success': False, 'message': 'Método no permitido'})

@require_admin
def semestres(request):
    # Obtener el username de la sesión
    username = request.session.get('username', 'admin')
    
    with connection.cursor() as cursor:
        # Obtener todos los semestres
        cursor.execute("""
            SELECT id, nombre, fecha_inicio, fecha_fin, activo, fecha_creacion,
                   DATEDIFF(fecha_fin, fecha_inicio) as duracion_dias
            FROM semestres 
            ORDER BY fecha_inicio DESC
        """)
        columns = [col[0] for col in cursor.description]
        semestres_data = [dict(zip(columns, row)) for row in cursor.fetchall()]
        
        # Obtener semestre activo
        cursor.execute("SELECT id, nombre FROM semestres WHERE activo = 1 LIMIT 1")
        semestre_actual_row = cursor.fetchone()
        semestre_actual = None
        if semestre_actual_row:
            semestre_actual = {
                'id': semestre_actual_row[0],
                'nombre': semestre_actual_row[1]
            }
        
    return render(request, 'admin/menu/semestres.html', {
        'semestres': semestres_data,
        'semestre_actual': semestre_actual,
        'user_name': username
    })
    
    
@require_admin
def grupos(request):
    # Obtener el username de la sesión
    username = request.session.get('username', 'admin')
    
    with connection.cursor() as cursor:
        # Obtener todos los grupos con información relacionada
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
                s.nombre as semestre_nombre,
                CONCAT(u.nombre, ' ', u.apellido) as profesor_nombre,
                g.materia_id,
                g.semestre_id,
                g.profesor_id
            FROM grupos g
            LEFT JOIN materias m ON g.materia_id = m.id
            LEFT JOIN semestres s ON g.semestre_id = s.id
            LEFT JOIN usuarios u ON g.profesor_id = u.id
            ORDER BY g.fecha_creacion DESC
        """)
        columns = [col[0] for col in cursor.description]
        grupos_data = [dict(zip(columns, row)) for row in cursor.fetchall()]
        
        # Obtener materias para el dropdown
        cursor.execute("SELECT id, nombre FROM materias ORDER BY nombre")
        materias = cursor.fetchall()
        
        # Obtener semestres para el dropdown
        cursor.execute("SELECT id, nombre FROM semestres ORDER BY fecha_inicio DESC")
        semestres = cursor.fetchall()
        
        # Obtener profesores para el dropdown
        cursor.execute("""
            SELECT id, CONCAT(nombre, ' ', apellido) as nombre_completo 
            FROM usuarios 
            WHERE rol = 'profesor' 
            ORDER BY nombre
        """)
        profesores = cursor.fetchall()
    
    return render(request, 'admin/menu/grupos.html', {
        'grupos': grupos_data,
        'materias': materias,
        'semestres': semestres,
        'profesores': profesores,
        'user_name': username  # ← AGREGAR ESTA LÍNEA
    })

@require_admin
@csrf_exempt
def crear_grupo(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            nombre = data.get('nombre', '').strip()
            descripcion = data.get('descripcion', '').strip()
            materia_id = data.get('materia_id')
            semestre_id = data.get('semestre_id')
            profesor_id = data.get('profesor_id')
            turno = data.get('turno', 'matutino')
            fecha_inicio = data.get('fecha_inicio')
            fecha_fin = data.get('fecha_fin')
            activo = data.get('activo', True)
            
            # Validaciones
            if not all([nombre, materia_id, semestre_id, profesor_id, turno]):
                return JsonResponse({'success': False, 'message': 'Nombre, materia, semestre, profesor y turno son obligatorios'})
            
            # Validar fechas si están presentes
            fecha_inicio_dt = None
            fecha_fin_dt = None
            
            if fecha_inicio:
                try:
                    fecha_inicio_dt = datetime.strptime(fecha_inicio, '%Y-%m-%d').date()
                except ValueError:
                    return JsonResponse({'success': False, 'message': 'Formato de fecha de inicio inválido'})
            
            if fecha_fin:
                try:
                    fecha_fin_dt = datetime.strptime(fecha_fin, '%Y-%m-%d').date()
                except ValueError:
                    return JsonResponse({'success': False, 'message': 'Formato de fecha de fin inválido'})
            
            if fecha_inicio_dt and fecha_fin_dt and fecha_inicio_dt >= fecha_fin_dt:
                return JsonResponse({'success': False, 'message': 'La fecha de fin debe ser posterior a la fecha de inicio'})
            
            with connection.cursor() as cursor:
                # Verificar si ya existe un grupo con ese nombre en el mismo semestre
                cursor.execute("""
                    SELECT id FROM grupos 
                    WHERE nombre = %s AND semestre_id = %s
                """, [nombre, semestre_id])
                
                if cursor.fetchone():
                    return JsonResponse({
                        'success': False, 
                        'message': 'Ya existe un grupo con ese nombre en este semestre'
                    })
                
                # Insertar nuevo grupo
                cursor.execute("""
                    INSERT INTO grupos 
                    (nombre, descripcion, materia_id, semestre_id, profesor_id, 
                     turno, fecha_inicio, fecha_fin, activo) 
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                """, [
                    nombre, 
                    descripcion if descripcion else None,
                    materia_id,
                    semestre_id,
                    profesor_id,
                    turno,
                    fecha_inicio_dt,
                    fecha_fin_dt,
                    1 if activo else 0
                ])
                
                return JsonResponse({'success': True, 'message': 'Grupo creado exitosamente'})
                
        except Exception as e:
            return JsonResponse({'success': False, 'message': f'Error al crear grupo: {str(e)}'})
    
    return JsonResponse({'success': False, 'message': 'Método no permitido'})

@require_admin
@csrf_exempt
def actualizar_grupo(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            grupo_id = data.get('grupo_id')
            nombre = data.get('nombre', '').strip()
            descripcion = data.get('descripcion', '').strip()
            materia_id = data.get('materia_id')
            semestre_id = data.get('semestre_id')
            profesor_id = data.get('profesor_id')
            turno = data.get('turno', 'matutino')
            fecha_inicio = data.get('fecha_inicio')
            fecha_fin = data.get('fecha_fin')
            activo = data.get('activo', True)
            
            if not all([nombre, materia_id, semestre_id, profesor_id, turno]):
                return JsonResponse({'success': False, 'message': 'Nombre, materia, semestre, profesor y turno son obligatorios'})
            
            # Validar fechas si están presentes
            fecha_inicio_dt = None
            fecha_fin_dt = None
            
            if fecha_inicio:
                try:
                    fecha_inicio_dt = datetime.strptime(fecha_inicio, '%Y-%m-%d').date()
                except ValueError:
                    return JsonResponse({'success': False, 'message': 'Formato de fecha de inicio inválido'})
            
            if fecha_fin:
                try:
                    fecha_fin_dt = datetime.strptime(fecha_fin, '%Y-%m-%d').date()
                except ValueError:
                    return JsonResponse({'success': False, 'message': 'Formato de fecha de fin inválido'})
            
            if fecha_inicio_dt and fecha_fin_dt and fecha_inicio_dt >= fecha_fin_dt:
                return JsonResponse({'success': False, 'message': 'La fecha de fin debe ser posterior a la fecha de inicio'})
            
            with connection.cursor() as cursor:
                # Verificar si ya existe otro grupo con ese nombre en el mismo semestre
                cursor.execute("""
                    SELECT id FROM grupos 
                    WHERE nombre = %s AND semestre_id = %s AND id != %s
                """, [nombre, semestre_id, grupo_id])
                
                if cursor.fetchone():
                    return JsonResponse({
                        'success': False, 
                        'message': 'Ya existe otro grupo con ese nombre en este semestre'
                    })
                
                # Actualizar grupo
                cursor.execute("""
                    UPDATE grupos SET 
                    nombre = %s, 
                    descripcion = %s, 
                    materia_id = %s, 
                    semestre_id = %s, 
                    profesor_id = %s, 
                    turno = %s, 
                    fecha_inicio = %s, 
                    fecha_fin = %s, 
                    activo = %s 
                    WHERE id = %s
                """, [
                    nombre,
                    descripcion if descripcion else None,
                    materia_id,
                    semestre_id,
                    profesor_id,
                    turno,
                    fecha_inicio_dt,
                    fecha_fin_dt,
                    1 if activo else 0,
                    grupo_id
                ])
                
                return JsonResponse({'success': True, 'message': 'Grupo actualizado exitosamente'})
                
        except Exception as e:
            return JsonResponse({'success': False, 'message': f'Error al actualizar grupo: {str(e)}'})
    
    return JsonResponse({'success': False, 'message': 'Método no permitido'})

@require_admin
@csrf_exempt
def eliminar_grupo(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            grupo_id = data.get('grupo_id')
            
            with connection.cursor() as cursor:
                # Verificar que el grupo existe
                cursor.execute("SELECT nombre FROM grupos WHERE id = %s", [grupo_id])
                result = cursor.fetchone()
                
                if not result:
                    return JsonResponse({'success': False, 'message': 'Grupo no encontrado'})
                
                # Verificar si hay estudiantes asociados al grupo
                cursor.execute("SELECT COUNT(*) FROM estudiante_grupos WHERE grupo_id = %s", [grupo_id])
                estudiantes_count = cursor.fetchone()[0]
                
                if estudiantes_count > 0:
                    return JsonResponse({
                        'success': False, 
                        'message': f'No se puede eliminar el grupo porque tiene {estudiantes_count} estudiantes asociados'
                    })
                
                # Eliminar grupo
                cursor.execute("DELETE FROM grupos WHERE id = %s", [grupo_id])
                
                return JsonResponse({'success': True, 'message': 'Grupo eliminado exitosamente'})
                
        except Exception as e:
            return JsonResponse({'success': False, 'message': f'Error al eliminar grupo: {str(e)}'})
    
    return JsonResponse({'success': False, 'message': 'Método no permitido'})

@require_admin
@csrf_exempt
def toggle_grupo(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            grupo_id = data.get('grupo_id')
            
            with connection.cursor() as cursor:
                # Obtener estado actual
                cursor.execute("SELECT activo FROM grupos WHERE id = %s", [grupo_id])
                result = cursor.fetchone()
                
                if not result:
                    return JsonResponse({'success': False, 'message': 'Grupo no encontrado'})
                
                nuevo_estado = 0 if result[0] == 1 else 1
                
                # Actualizar estado del grupo
                cursor.execute("UPDATE grupos SET activo = %s WHERE id = %s", [nuevo_estado, grupo_id])
                
                estado_texto = "activado" if nuevo_estado == 1 else "desactivado"
                return JsonResponse({'success': True, 'message': f'Grupo {estado_texto} exitosamente'})
                
        except Exception as e:
            return JsonResponse({'success': False, 'message': f'Error al cambiar estado del grupo: {str(e)}'})
    
    return JsonResponse({'success': False, 'message': 'Método no permitido'})







# Funciones para la sección de perfil, son 3, esta y la de actualizar y cambiar password:
def perfil_usuario(request):
    """
    Vista para mostrar el perfil del usuario con las opciones de gestión
    """
    # Verificar si hay sesión activa
    if not request.session.get('user_id'):
        return redirect('login:login_view')
    
    user_id = request.session.get('user_id')
    
    with connection.cursor() as cursor:
        # Obtener todos los datos del usuario
        cursor.execute("""
            SELECT id, nombre, apellido, email, rol, fecha_creacion, 
                   numero_cuenta, perfil_completado, telefono, usuario
            FROM usuarios 
            WHERE id = %s
        """, [user_id])
        
        result = cursor.fetchone()
        if not result:
            return redirect('login:login_view')
        
        columns = [col[0] for col in cursor.description]
        usuario = dict(zip(columns, result))
    
    # Definir las acciones disponibles según el rol
    acciones_disponibles = []
    user_role = usuario['rol']
    
    if user_role == 'administrador':
        acciones_disponibles = [
            {'nombre': 'Gestionar Usuarios', 'url': 'administradores:usuarios', 'icono': 'fas fa-users'},
            {'nombre': 'Gestionar Materias', 'url': 'administradores:materias', 'icono': 'fas fa-book'},
            {'nombre': 'Gestionar Grupos', 'url': 'administradores:grupos', 'icono': 'fas fa-chalkboard-teacher'},
            {'nombre': 'Gestionar Semestres', 'url': 'administradores:semestres', 'icono': 'fas fa-calendar-alt'},
        ]
    elif user_role == 'profesor':
        acciones_disponibles = [
            {'nombre': 'Mis Grupos', 'url': 'profesor:grupos', 'icono': 'fas fa-chalkboard-teacher'},
            {'nombre': 'Calificaciones', 'url': 'profesor:calificaciones', 'icono': 'fas fa-chart-bar'},
        ]
    elif user_role == 'estudiante':
        acciones_disponibles = [
            {'nombre': 'Mis Materias', 'url': 'estudiante:materias', 'icono': 'fas fa-book'},
            {'nombre': 'Mis Calificaciones', 'url': 'estudiante:calificaciones', 'icono': 'fas fa-graduation-cap'},
        ]
    
    context = {
        'usuario': usuario,
        'acciones': acciones_disponibles,
    }
    
    return render(request, 'admin/menu/perfil_usuario.html', context)



@csrf_exempt
def actualizar_perfil(request):
    if request.method == 'POST':
        try:
            user_id = request.POST.get('user_id')
            nombre = request.POST.get('nombre', '').strip()
            apellido = request.POST.get('apellido', '').strip()
            usuario = request.POST.get('usuario', '').strip()
            email = request.POST.get('email', '').strip()
            telefono = request.POST.get('telefono', '').strip()
            
            # Validaciones básicas
            if not all([nombre, apellido, usuario, email, telefono]):
                messages.error(request, 'Todos los campos son obligatorios')
                return redirect('administradores:perfil_usuario')
            
            # Validar formato de email
            import re
            if not re.match(r'^[^\s@]+@[^\s@]+\.[^\s@]+$', email):
                messages.error(request, 'Formato de correo electrónico inválido')
                return redirect('administradores:perfil_usuario')
            
            # Validar formato de teléfono
            if not re.match(r'^[0-9]{10}$', telefono):
                messages.error(request, 'El teléfono debe tener exactamente 10 dígitos')
                return redirect('administradores:perfil_usuario')
            
            with connection.cursor() as cursor:
                # Verificar que el email y usuario no estén en uso por otro usuario
                cursor.execute("""
                    SELECT id FROM usuarios 
                    WHERE (email = %s OR usuario = %s) AND id != %s
                """, [email, usuario, user_id])
                
                if cursor.fetchone():
                    messages.error(request, 'El correo electrónico o nombre de usuario ya está en uso')
                    return redirect('administradores:perfil_usuario')
                
                # Actualizar usuario
                cursor.execute("""
                    UPDATE usuarios 
                    SET nombre = %s, apellido = %s, usuario = %s, 
                        email = %s, telefono = %s
                    WHERE id = %s
                """, [nombre, apellido, usuario, email, telefono, user_id])
                
                # Actualizar la sesión
                request.session['username'] = usuario
                request.session['email'] = email
                
                messages.success(request, 'Perfil actualizado exitosamente')
                return redirect('administradores:perfil_usuario')
                
        except Exception as e:
            messages.error(request, f'Error al actualizar perfil: {str(e)}')
            return redirect('administradores:perfil_usuario')
    
    return redirect('administradores:perfil_usuario')

@csrf_exempt
def cambiar_password(request):
    if request.method == 'POST':
        try:
            user_id = request.POST.get('user_id')
            nueva_password = request.POST.get('nueva_password')
            confirmar_password = request.POST.get('confirmar_password')
            
            # Validaciones
            if not nueva_password or not confirmar_password:
                messages.error(request, 'Ambos campos de contraseña son obligatorios')
                return redirect('administradores:perfil_usuario')
            
            if len(nueva_password) < 8:
                messages.error(request, 'La contraseña debe tener al menos 8 caracteres')
                return redirect('administradores:perfil_usuario')
            
            if nueva_password != confirmar_password:
                messages.error(request, 'Las contraseñas no coinciden')
                return redirect('administradores:perfil_usuario')
            
            # Hashear la contraseña
            import hashlib
            password_hash = hashlib.sha256(nueva_password.encode()).hexdigest()
            
            with connection.cursor() as cursor:
                cursor.execute("""
                    UPDATE usuarios 
                    SET password_hash = %s
                    WHERE id = %s
                """, [password_hash, user_id])
                
                messages.success(request, 'Contraseña cambiada exitosamente')
                return redirect('administradores:perfil_usuario')
                
        except Exception as e:
            messages.error(request, f'Error al cambiar contraseña: {str(e)}')
            return redirect('administradores:perfil_usuario')
    
    return redirect('administradores:perfil_usuario')
















