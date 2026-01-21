# administradores/context_processors.py
from django.db import connection

def usuario_context(request):
    """
    Context processor para agregar datos del usuario logueado a todas las plantillas
    """
    if not request.session.get('user_id'):
        return {'usuario_actual': None}
    
    user_id = request.session.get('user_id')
    
    try:
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT id, nombre, apellido, email, rol, fecha_creacion, 
                       numero_cuenta, perfil_completado, telefono, usuario, icono_user
                FROM usuarios 
                WHERE id = %s
            """, [user_id])
            
            result = cursor.fetchone()
            if result:
                columns = [col[0] for col in cursor.description]
                usuario_actual = dict(zip(columns, result))
                return {'usuario_actual': usuario_actual}
    except Exception:
        pass
    
    return {'usuario_actual': None}