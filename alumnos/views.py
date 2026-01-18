from django.shortcuts import render, redirect
from django.contrib import messages
from functools import wraps
from django.db import connection
import hashlib
import secrets
import string
import re

def login_required_session(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.session.get('user_id'):
            messages.error(request, 'Por favor inicia sesión')
            return redirect('login:login_view')
        return view_func(request, *args, **kwargs)
    return wrapper

def ejecutar_consulta(query, params=None, fetchone=False):
    """Función auxiliar para ejecutar consultas SQL"""
    with connection.cursor() as cursor:
        cursor.execute(query, params or ())
        if fetchone:
            return cursor.fetchone()
        return cursor.fetchall()

# FUNCIONES DE CONTRASEÑA COPIADAS DE TU LOGIN/VIEWS.PY
def verificar_password(password_ingresada, password_hash_almacenado):
    """
    Verifica si la contraseña ingresada coincide con el hash almacenado.
    El hash debe tener el formato: scrypt:16384:8:1$salt$hash
    """
    try:
        # Separar los componentes del hash almacenado
        partes = password_hash_almacenado.split('$')
        
        if len(partes) != 3:
            print(f"Formato de hash inválido: {password_hash_almacenado}")
            return False
        
        algoritmo_params, salt, hash_almacenado = partes
        
        # Verificar que sea scrypt
        if not algoritmo_params.startswith('scrypt:'):
            print(f"Algoritmo no soportado: {algoritmo_params}")
            return False
        
        # Extraer parámetros (n, r, p)
        params = algoritmo_params.split(':')
        n = int(params[1])
        r = int(params[2])
        p = int(params[3])
        
        # Generar hash con la contraseña ingresada usando el mismo salt
        password_hash_nuevo = hashlib.scrypt(
            password_ingresada.encode('utf-8'),
            salt=salt.encode('utf-8'),
            n=n,
            r=r,
            p=p,
            dklen=64
        )
        
        hash_nuevo_hex = password_hash_nuevo.hex()
        
        # Comparar los hashes de forma segura
        return secrets.compare_digest(hash_nuevo_hex, hash_almacenado)
        
    except Exception as e:
        print(f"Error al verificar contraseña: {e}")
        return False

def generar_hash_scrypt(password):
    """Genera un hash scrypt compatible con el sistema actual"""
    salt = secrets.token_hex(16)
    
    password_hash = hashlib.scrypt(
        password.encode('utf-8'),
        salt=salt.encode('utf-8'),
        n=16384,  # Mismo que en tu login
        r=8,      # Mismo que en tu login
        p=1,      # Mismo que en tu login
        dklen=64  # Mismo que en tu login
    )
    
    hash_hex = password_hash.hex()
    return f"scrypt:16384:8:1${salt}${hash_hex}"

@login_required_session
def alumnos(request):
    user_id = request.session.get('user_id')
    
    try:
        # Obtener usuario de la base de datos usando diccionario
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM usuarios WHERE id = %s", [user_id])
            columns = [col[0] for col in cursor.description]
            usuario_row = cursor.fetchone()
            
            if not usuario_row:
                messages.error(request, 'Usuario no encontrado')
                return redirect('login:login_view')
            
            usuario = dict(zip(columns, usuario_row))
        
        # Obtener perfil del estudiante
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM perfiles_estudiante WHERE estudiante_id = %s", [user_id])
            columns = [col[0] for col in cursor.description]
            perfil_row = cursor.fetchone()
            perfil = dict(zip(columns, perfil_row)) if perfil_row else None
        
        # Construir contexto
        nombre = usuario.get('nombre', '')
        apellido = usuario.get('apellido', '')
        email = usuario.get('email', '')
        rol = usuario.get('rol', 'estudiante')
        username = usuario.get('usuario', '')
        numero_cuenta = usuario.get('numero_cuenta', '')
        telefono = usuario.get('telefono', '')
        
        # Obtener datos del perfil si existe
        semestre = perfil.get('semestre', 1) if perfil else 1
        facultad = perfil.get('facultad', 'FES Cuautitlán') if perfil else 'FES Cuautitlán'
        carrera = perfil.get('carrera', 'Informática') if perfil else 'Informática'
        
        context = {
            'user_name': f"{nombre} {apellido}".strip() or 'Usuario',
            'user_email': email,
            'user_role': rol,
            'username': username,
            'numero_cuenta': numero_cuenta or 'No asignado',
            'semestre': semestre,
            'facultad': facultad,
            'carrera': carrera,
            'telefono': telefono or 'No registrado',
        }
        
    except Exception as e:
        messages.error(request, f'Error al cargar datos: {str(e)}')
        context = {
            'user_name': request.session.get('user_name', 'Usuario'),
            'user_email': request.session.get('user_email', ''),
            'user_role': request.session.get('user_role', 'estudiante'),
            'username': request.session.get('username', ''),
            'numero_cuenta': request.session.get('numero_cuenta', ''),
            'semestre': 1,
            'facultad': 'FES Cuautitlán',
            'carrera': 'Informática',
            'telefono': 'No registrado',
        }
    
    return render(request, 'alumnos/alumnos.html', context)

@login_required_session
def editar_perfil(request):
    user_id = request.session.get('user_id')
    
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        apellido = request.POST.get('apellido')
        email = request.POST.get('email')
        telefono = request.POST.get('telefono')
        semestre = request.POST.get('semestre')
        facultad = request.POST.get('facultad')
        carrera = request.POST.get('carrera')
        
        # Si seleccionó "otra" en carrera, usar el campo personalizado
        if carrera == 'otra':
            carrera = request.POST.get('carrera_otra', 'Otra')
        
        # Si seleccionó "otra" en facultad, usar el campo personalizado
        if facultad == 'otra':
            facultad = request.POST.get('facultad_otra', 'Otra')
        
        # Validaciones
        if not nombre or not apellido or not email:
            messages.error(request, 'Nombre, apellido y email son obligatorios')
            return redirect('alumnos:editar_perfil')
        
        try:
            # Verificar si el email ya existe (excluyendo al usuario actual)
            with connection.cursor() as cursor:
                cursor.execute(
                    "SELECT id FROM usuarios WHERE email = %s AND id != %s",
                    [email, user_id]
                )
                email_existente = cursor.fetchone()
            
            if email_existente:
                messages.error(request, 'El email ya está registrado por otro usuario')
                return redirect('alumnos:editar_perfil')
            
            # Actualizar usuario en la base de datos
            ejecutar_consulta(
                """
                UPDATE usuarios 
                SET nombre = %s, apellido = %s, email = %s, telefono = %s 
                WHERE id = %s
                """,
                [nombre, apellido, email, telefono, user_id]
            )
            
            # Verificar si existe perfil
            perfil_existente = ejecutar_consulta(
                "SELECT id FROM perfiles_estudiante WHERE estudiante_id = %s",
                [user_id],
                fetchone=True
            )
            
            if perfil_existente:
                # Actualizar perfil existente
                ejecutar_consulta(
                    """
                    UPDATE perfiles_estudiante 
                    SET semestre = %s, facultad = %s, carrera = %s, 
                        fecha_actualizacion = NOW() 
                    WHERE estudiante_id = %s
                    """,
                    [semestre, facultad, carrera, user_id]
                )
            else:
                # Crear nuevo perfil
                ejecutar_consulta(
                    """
                    INSERT INTO perfiles_estudiante 
                    (estudiante_id, semestre, facultad, carrera, fecha_creacion, fecha_actualizacion)
                    VALUES (%s, %s, %s, %s, NOW(), NOW())
                    """,
                    [user_id, semestre, facultad, carrera]
                )
            
            # Actualizar sesión
            request.session['user_name'] = f"{nombre} {apellido}"
            request.session['user_email'] = email
            
            messages.success(request, 'Perfil actualizado correctamente')
            return redirect('alumnos:alumnos')
            
        except Exception as e:
            messages.error(request, f'Error al actualizar el perfil: {str(e)}')
            return redirect('alumnos:editar_perfil')
    
    # Obtener datos actuales para el formulario
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM usuarios WHERE id = %s", [user_id])
            columns = [col[0] for col in cursor.description]
            usuario_row = cursor.fetchone()
            
            if not usuario_row:
                messages.error(request, 'Usuario no encontrado')
                return redirect('alumnos:alumnos')
            
            usuario = dict(zip(columns, usuario_row))
        
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM perfiles_estudiante WHERE estudiante_id = %s", [user_id])
            columns = [col[0] for col in cursor.description]
            perfil_row = cursor.fetchone()
            perfil = dict(zip(columns, perfil_row)) if perfil_row else None
        
        context = {
            'user_name': usuario.get('nombre', ''),
            'user_lastname': usuario.get('apellido', ''),
            'user_email': usuario.get('email', ''),
            'numero_cuenta': usuario.get('numero_cuenta', ''),
            'telefono': usuario.get('telefono', '') or '',
            'carrera': perfil.get('carrera', 'Informática') if perfil else 'Informática',
            'semestre': perfil.get('semestre', 1) if perfil else 1,
            'facultad': perfil.get('facultad', 'FES Cuautitlán') if perfil else 'FES Cuautitlán',
        }
        
    except Exception as e:
        messages.error(request, f'Error al cargar datos: {str(e)}')
        context = {
            'user_name': '',
            'user_lastname': '',
            'user_email': '',
            'numero_cuenta': '',
            'telefono': '',
            'carrera': 'Informática',
            'semestre': 1,
            'facultad': 'FES Cuautitlán',
        }
    
    return render(request, 'alumnos/editar_perfil.html', context)

@login_required_session
def cambiar_password(request):
    user_id = request.session.get('user_id')
    
    if request.method == 'POST':
        current_password = request.POST.get('current_password')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')
        
        # Validaciones básicas
        if not current_password or not new_password or not confirm_password:
            messages.error(request, 'Todos los campos son obligatorios')
            return redirect('alumnos:cambiar_password')
        
        if new_password != confirm_password:
            messages.error(request, 'Las contraseñas nuevas no coinciden')
            return redirect('alumnos:cambiar_password')
        
        if len(new_password) < 8:
            messages.error(request, 'La contraseña debe tener al menos 8 caracteres')
            return redirect('alumnos:cambiar_password')
        
        # Validaciones adicionales de seguridad
        if not any(c.isupper() for c in new_password):
            messages.error(request, 'La contraseña debe contener al menos una letra mayúscula')
            return redirect('alumnos:cambiar_password')
        
        if not any(c.islower() for c in new_password):
            messages.error(request, 'La contraseña debe contener al menos una letra minúscula')
            return redirect('alumnos:cambiar_password')
        
        if not any(c.isdigit() for c in new_password):
            messages.error(request, 'La contraseña debe contener al menos un número')
            return redirect('alumnos:cambiar_password')
        
        try:
            # Obtener hash de contraseña actual
            with connection.cursor() as cursor:
                cursor.execute("SELECT password_hash FROM usuarios WHERE id = %s", [user_id])
                result = cursor.fetchone()
                
                if not result:
                    messages.error(request, 'Usuario no encontrado')
                    return redirect('alumnos:cambiar_password')
                
                password_hash = result[0]
            
            print(f"DEBUG - Hash almacenado para usuario {user_id}: {password_hash[:100]}...")  # Para debug
            
            # Verificar contraseña actual usando la MISMA función que en login
            if not verificar_password(current_password, password_hash):
                messages.error(request, 'La contraseña actual es incorrecta')
                return redirect('alumnos:cambiar_password')
            
            # Generar nuevo hash usando la MISMA función que en registro
            new_password_hash = generar_hash_scrypt(new_password)
            print(f"DEBUG - Nuevo hash generado: {new_password_hash[:100]}...")  # Para debug
            
            # Actualizar contraseña en la base de datos
            with connection.cursor() as cursor:
                cursor.execute(
                    "UPDATE usuarios SET password_hash = %s WHERE id = %s",
                    [new_password_hash, user_id]
                )
                affected_rows = cursor.rowcount
            
            print(f"DEBUG - Filas actualizadas: {affected_rows}")  # Para debug
            
            if affected_rows == 0:
                messages.error(request, 'No se pudo actualizar la contraseña')
                return redirect('alumnos:cambiar_password')
            
            # Verificar que el nuevo hash funciona
            print(f"DEBUG - Verificando nuevo hash...")
            if not verificar_password(new_password, new_password_hash):
                print(f"DEBUG - ¡ERROR! El nuevo hash no verifica con la nueva contraseña!")
                messages.error(request, 'Error interno al verificar la nueva contraseña')
                return redirect('alumnos:cambiar_password')
            
            messages.success(request, 'Contraseña actualizada correctamente')
            return redirect('alumnos:alumnos')
            
        except Exception as e:
            print(f"DEBUG - Error detallado: {str(e)}")  # Para debug
            import traceback
            traceback.print_exc()
            messages.error(request, f'Error al cambiar la contraseña: {str(e)}')
            return redirect('alumnos:cambiar_password')
    
    return render(request, 'alumnos/cambiar_password.html')

@login_required_session
def info_sistema(request):
    user_id = request.session.get('user_id')
    
    try:
        # Obtener usuario
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM usuarios WHERE id = %s", [user_id])
            columns = [col[0] for col in cursor.description]
            usuario_row = cursor.fetchone()
            
            if not usuario_row:
                messages.error(request, 'Usuario no encontrado')
                return redirect('alumnos:alumnos')
            
            usuario = dict(zip(columns, usuario_row))
        
        # Obtener perfil
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM perfiles_estudiante WHERE estudiante_id = %s", [user_id])
            columns = [col[0] for col in cursor.description]
            perfil_row = cursor.fetchone()
            perfil = dict(zip(columns, perfil_row)) if perfil_row else None
        
        # Obtener fecha de registro
        with connection.cursor() as cursor:
            cursor.execute("SELECT DATE(fecha_creacion) FROM usuarios WHERE id = %s", [user_id])
            fecha_registro = cursor.fetchone()
        
        fecha_formateada = ''
        if fecha_registro and fecha_registro[0]:
            try:
                meses = {
                    1: 'enero', 2: 'febrero', 3: 'marzo', 4: 'abril',
                    5: 'mayo', 6: 'junio', 7: 'julio', 8: 'agosto',
                    9: 'septiembre', 10: 'octubre', 11: 'noviembre', 12: 'diciembre'
                }
                fecha = fecha_registro[0]
                fecha_formateada = f"{fecha.day} de {meses[fecha.month]}, {fecha.year}"
            except:
                fecha_formateada = str(fecha_registro[0])
        else:
            fecha_formateada = 'No disponible'
        
        context = {
            'version_sistema': '2.0.1',
            'ultima_actualizacion': '15 de Enero, 2025',
            'soporte_email': 'soporte@intellitutor.unam.mx',
            'contacto_email': 'contacto@intellitutor.unam.mx',
            'terminos_url': '#',
            'politicas_url': '#',
            'user_role': usuario.get('rol', 'estudiante'),
            'fecha_registro': fecha_formateada,
            'estado_cuenta': 'Activa',
            'usuario': usuario.get('usuario', ''),
            'nombre_completo': f"{usuario.get('nombre', '')} {usuario.get('apellido', '')}".strip(),
            'email': usuario.get('email', ''),
            'semestre': perfil.get('semestre', 'No especificado') if perfil else 'No especificado',
            'carrera': perfil.get('carrera', 'No especificada') if perfil else 'No especificada',
        }
        
    except Exception as e:
        messages.error(request, f'Error al obtener información: {str(e)}')
        return redirect('alumnos:alumnos')
    
    return render(request, 'alumnos/info_sistema.html', context)

# Añade estas funciones al final de tu views.py (después de info_sistema):

@login_required_session
def mis_cursos(request):
    """
    Vista principal de cursos del estudiante.
    """
    user_id = request.session.get('user_id')
    
    try:
        # Obtener cursos/grupos en los que está inscrito el estudiante
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT 
                    g.id as grupo_id,
                    g.nombre as grupo_nombre,
                    g.descripcion as grupo_descripcion,
                    m.nombre as materia_nombre,
                    m.descripcion as materia_descripcion,
                    m.creditos,
                    s.nombre as semestre_nombre,
                    CONCAT(u.nombre, ' ', u.apellido) as profesor_nombre,
                    g.fecha_inicio,
                    g.fecha_fin,
                    g.turno,
                    g.activo
                FROM grupos g
                INNER JOIN grupo_estudiante ge ON g.id = ge.grupo_id
                INNER JOIN materias m ON g.materia_id = m.id
                INNER JOIN semestres s ON g.semestre_id = s.id
                INNER JOIN usuarios u ON g.profesor_id = u.id
                WHERE ge.estudiante_id = %s
                ORDER BY g.fecha_inicio DESC, g.nombre
            """, [user_id])
            
            columns = [col[0] for col in cursor.description]
            cursos = [dict(zip(columns, row)) for row in cursor.fetchall()]
        
        # Contar cursos activos vs finalizados
        cursos_activos = sum(1 for c in cursos if c.get('activo') == 1)
        cursos_finalizados = len(cursos) - cursos_activos
        
        # Obtener materias disponibles para inscripción
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT 
                    m.id as materia_id,
                    m.nombre as materia_nombre,
                    m.descripcion as materia_descripcion,
                    m.creditos,
                    COUNT(DISTINCT g.id) as grupos_disponibles
                FROM materias m
                LEFT JOIN grupos g ON m.id = g.materia_id AND g.activo = 1
                WHERE m.id NOT IN (
                    SELECT g2.materia_id 
                    FROM grupos g2
                    INNER JOIN grupo_estudiante ge2 ON g2.id = ge2.grupo_id
                    WHERE ge2.estudiante_id = %s
                )
                GROUP BY m.id, m.nombre, m.descripcion, m.creditos
                ORDER BY m.nombre
            """, [user_id])
            
            columns = [col[0] for col in cursor.description]
            materias_disponibles = [dict(zip(columns, row)) for row in cursor.fetchall()]
        
        context = {
            'cursos': cursos,
            'cursos_activos': cursos_activos,
            'cursos_finalizados': cursos_finalizados,
            'materias_disponibles': materias_disponibles,
            'total_cursos': len(cursos),
        }
        
    except Exception as e:
        messages.error(request, f'Error al cargar cursos: {str(e)}')
        context = {
            'cursos': [],
            'cursos_activos': 0,
            'cursos_finalizados': 0,
            'materias_disponibles': [],
            'total_cursos': 0,
        }
    
    return render(request, 'alumnos/mis_cursos.html', context)

@login_required_session
def detalle_curso(request, curso_id):
    """
    Vista detallada de un curso específico.
    """
    user_id = request.session.get('user_id')
    
    try:
        # Verificar que el estudiante está inscrito en el curso
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT COUNT(*) 
                FROM grupo_estudiante 
                WHERE grupo_id = %s AND estudiante_id = %s
            """, [curso_id, user_id])
            
            esta_inscrito = cursor.fetchone()[0] > 0
            
            if not esta_inscrito:
                messages.error(request, 'No estás inscrito en este curso')
                return redirect('alumnos:mis_cursos')
        
        # Obtener información detallada del curso
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT 
                    g.id as grupo_id,
                    g.nombre as grupo_nombre,
                    g.descripcion as grupo_descripcion,
                    m.id as materia_id,
                    m.nombre as materia_nombre,
                    m.descripcion as materia_descripcion,
                    m.creditos,
                    s.id as semestre_id,
                    s.nombre as semestre_nombre,
                    s.fecha_inicio as semestre_inicio,
                    s.fecha_fin as semestre_fin,
                    u.id as profesor_id,
                    CONCAT(u.nombre, ' ', u.apellido) as profesor_nombre,
                    u.email as profesor_email,
                    g.fecha_creacion,
                    g.fecha_inicio,
                    g.fecha_fin,
                    g.turno,
                    g.activo,
                    COUNT(DISTINCT ge.estudiante_id) as total_estudiantes
                FROM grupos g
                INNER JOIN materias m ON g.materia_id = m.id
                INNER JOIN semestres s ON g.semestre_id = s.id
                INNER JOIN usuarios u ON g.profesor_id = u.id
                LEFT JOIN grupo_estudiante ge ON g.id = ge.grupo_id
                WHERE g.id = %s
                GROUP BY g.id, m.id, s.id, u.id
            """, [curso_id])
            
            columns = [col[0] for col in cursor.description]
            curso_row = cursor.fetchone()
            
            if not curso_row:
                messages.error(request, 'Curso no encontrado')
                return redirect('alumnos:mis_cursos')
            
            curso = dict(zip(columns, curso_row))
        
        # Obtener prácticas asignadas para este curso
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT 
                    p.id,
                    p.titulo,
                    p.descripcion,
                    p.fecha_entrega,
                    p.tiempo_estimado,
                    p.estado,
                    p.tipo_asignacion,
                    n.nombre as nivel,
                    COALESCE(e.calificacion, 0) as calificacion,
                    e.estado as estado_entrega
                FROM practicas p
                LEFT JOIN niveles n ON p.nivel_id = n.id
                LEFT JOIN entregas e ON p.id = e.practica_id AND e.estudiante_id = %s
                WHERE p.grupo_id = %s
                ORDER BY p.fecha_entrega
            """, [user_id, curso_id])
            
            columns = [col[0] for col in cursor.description]
            practicas = [dict(zip(columns, row)) for row in cursor.fetchall()]
        
        # Obtener compañeros del curso
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT 
                    u.id,
                    CONCAT(u.nombre, ' ', u.apellido) as nombre_completo,
                    u.email,
                    u.usuario,
                    pe.semestre
                FROM usuarios u
                INNER JOIN grupo_estudiante ge ON u.id = ge.estudiante_id
                LEFT JOIN perfiles_estudiante pe ON u.id = pe.estudiante_id
                WHERE ge.grupo_id = %s AND u.id != %s
                ORDER BY u.nombre, u.apellido
            """, [curso_id, user_id])
            
            columns = [col[0] for col in cursor.description]
            companeros = [dict(zip(columns, row)) for row in cursor.fetchall()]
        
        context = {
            'curso': curso,
            'practicas': practicas,
            'companeros': companeros,
            'total_practicas': len(practicas),
            'total_companeros': len(companeros),
        }
        
    except Exception as e:
        messages.error(request, f'Error al cargar el curso: {str(e)}')
        return redirect('alumnos:mis_cursos')
    
    return render(request, 'alumnos/detalle_curso.html', context)

@login_required_session
def cursos_disponibles(request):
    """
    Vista para ver cursos disponibles para inscripción.
    """
    user_id = request.session.get('user_id')
    
    try:
        # Obtener semestres activos
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT id, nombre, fecha_inicio, fecha_fin 
                FROM semestres 
                WHERE activo = 1 
                ORDER BY fecha_inicio DESC
            """)
            
            columns = [col[0] for col in cursor.description]
            semestres = [dict(zip(columns, row)) for row in cursor.fetchall()]
        
        # Obtener todos los grupos disponibles (no inscrito y activos)
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT 
                    g.id as grupo_id,
                    g.nombre as grupo_nombre,
                    g.descripcion as grupo_descripcion,
                    m.id as materia_id,
                    m.nombre as materia_nombre,
                    m.descripcion as materia_descripcion,
                    m.creditos,
                    s.nombre as semestre_nombre,
                    CONCAT(u.nombre, ' ', u.apellido) as profesor_nombre,
                    g.fecha_inicio,
                    g.fecha_fin,
                    g.turno,
                    COUNT(DISTINCT ge.estudiante_id) as estudiantes_inscritos,
                    CASE 
                        WHEN ge2.estudiante_id IS NOT NULL THEN 1
                        ELSE 0
                    END as ya_inscrito
                FROM grupos g
                INNER JOIN materias m ON g.materia_id = m.id
                INNER JOIN semestres s ON g.semestre_id = s.id
                INNER JOIN usuarios u ON g.profesor_id = u.id
                LEFT JOIN grupo_estudiante ge ON g.id = ge.grupo_id
                LEFT JOIN grupo_estudiante ge2 ON g.id = ge2.grupo_id AND ge2.estudiante_id = %s
                WHERE g.activo = 1 
                GROUP BY g.id, m.id, s.id, u.id, ge2.estudiante_id
                HAVING ya_inscrito = 0
                ORDER BY s.fecha_inicio DESC, m.nombre, g.nombre
            """, [user_id])
            
            columns = [col[0] for col in cursor.description]
            cursos_disponibles = [dict(zip(columns, row)) for row in cursor.fetchall()]
        
        # Obtener materias para filtro
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT DISTINCT m.id, m.nombre 
                FROM materias m
                INNER JOIN grupos g ON m.id = g.materia_id
                WHERE g.activo = 1
                ORDER BY m.nombre
            """)
            
            materias = [dict(id=row[0], nombre=row[1]) for row in cursor.fetchall()]
        
        context = {
            'cursos_disponibles': cursos_disponibles,
            'semestres': semestres,
            'materias': materias,
            'total_disponibles': len(cursos_disponibles),
        }
        
    except Exception as e:
        messages.error(request, f'Error al cargar cursos disponibles: {str(e)}')
        context = {
            'cursos_disponibles': [],
            'semestres': [],
            'materias': [],
            'total_disponibles': 0,
        }
    
    return render(request, 'alumnos/cursos_disponibles.html', context)

@login_required_session
def solicitar_inscripcion(request, grupo_id):
    """
    Vista para solicitar inscripción a un curso.
    """
    user_id = request.session.get('user_id')
    
    if request.method == 'POST':
        try:
            # Verificar que el grupo existe y está activo
            with connection.cursor() as cursor:
                cursor.execute("""
                    SELECT id, nombre, activo 
                    FROM grupos 
                    WHERE id = %s AND activo = 1
                """, [grupo_id])
                
                grupo = cursor.fetchone()
                
                if not grupo:
                    messages.error(request, 'El curso no está disponible para inscripción')
                    return redirect('alumnos:cursos_disponibles')
            
            # Verificar que no está ya inscrito
            with connection.cursor() as cursor:
                cursor.execute("""
                    SELECT id 
                    FROM grupo_estudiante 
                    WHERE grupo_id = %s AND estudiante_id = %s
                """, [grupo_id, user_id])
                
                if cursor.fetchone():
                    messages.warning(request, 'Ya estás inscrito en este curso')
                    return redirect('alumnos:mis_cursos')
            
            # Insertar la inscripción
            with connection.cursor() as cursor:
                cursor.execute("""
                    INSERT INTO grupo_estudiante (grupo_id, estudiante_id, fecha_inscripcion)
                    VALUES (%s, %s, NOW())
                """, [grupo_id, user_id])
            
            messages.success(request, '¡Inscripción solicitada correctamente!')
            return redirect('alumnos:mis_cursos')
            
        except Exception as e:
            messages.error(request, f'Error al solicitar inscripción: {str(e)}')
            return redirect('alumnos:cursos_disponibles')
    
    # GET request - mostrar confirmación
    try:
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT 
                    g.nombre as grupo_nombre,
                    m.nombre as materia_nombre,
                    CONCAT(u.nombre, ' ', u.apellido) as profesor_nombre,
                    g.descripcion
                FROM grupos g
                INNER JOIN materias m ON g.materia_id = m.id
                INNER JOIN usuarios u ON g.profesor_id = u.id
                WHERE g.id = %s
            """, [grupo_id])
            
            curso = cursor.fetchone()
            
            if not curso:
                messages.error(request, 'Curso no encontrado')
                return redirect('alumnos:cursos_disponibles')
            
            context = {
                'grupo_id': grupo_id,
                'grupo_nombre': curso[0],
                'materia_nombre': curso[1],
                'profesor_nombre': curso[2],
                'descripcion': curso[3],
            }
            
    except Exception as e:
        messages.error(request, f'Error: {str(e)}')
        return redirect('alumnos:cursos_disponibles')
    
    return render(request, 'alumnos/solicitar_inscripcion.html', context)

@login_required_session
def abandonar_curso(request, curso_id):
    """
    Vista para abandonar un curso.
    """
    user_id = request.session.get('user_id')
    
    if request.method == 'POST':
        try:
            # Verificar que está inscrito
            with connection.cursor() as cursor:
                cursor.execute("""
                    SELECT id 
                    FROM grupo_estudiante 
                    WHERE grupo_id = %s AND estudiante_id = %s
                """, [curso_id, user_id])
                
                if not cursor.fetchone():
                    messages.error(request, 'No estás inscrito en este curso')
                    return redirect('alumnos:mis_cursos')
            
            # Eliminar la inscripción
            with connection.cursor() as cursor:
                cursor.execute("""
                    DELETE FROM grupo_estudiante 
                    WHERE grupo_id = %s AND estudiante_id = %s
                """, [curso_id, user_id])
            
            messages.success(request, 'Has abandonado el curso correctamente')
            return redirect('alumnos:mis_cursos')
            
        except Exception as e:
            messages.error(request, f'Error al abandonar el curso: {str(e)}')
            return redirect('alumnos:detalle_curso', curso_id=curso_id)
    
    # GET request - mostrar confirmación
    try:
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT g.nombre, m.nombre 
                FROM grupos g
                INNER JOIN materias m ON g.materia_id = m.id
                WHERE g.id = %s
            """, [curso_id])
            
            curso = cursor.fetchone()
            
            if not curso:
                messages.error(request, 'Curso no encontrado')
                return redirect('alumnos:mis_cursos')
            
            context = {
                'curso_id': curso_id,
                'grupo_nombre': curso[0],
                'materia_nombre': curso[1],
            }
            
    except Exception as e:
        messages.error(request, f'Error: {str(e)}')
        return redirect('alumnos:mis_cursos')
    
    return render(request, 'alumnos/abandonar_curso.html', context)