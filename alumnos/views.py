from django.shortcuts import render, redirect
from django.contrib import messages
from functools import wraps


def login_required_session(view_func):
    """
    Decorador que requiere autenticación por sesión personalizada.
    Similar a @login_required pero para sesiones personalizadas.
    """
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.session.get('user_id'):
            messages.error(request, 'Por favor inicia sesión')
            return redirect('login:login_view')
        return view_func(request, *args, **kwargs)
    return wrapper

@login_required_session
def alumnos(request):
    # Verificar si el usuario está autenticado por sesión
    # (Ya verificado por el decorador)
    
    # Obtener datos del usuario de la sesión
    user_name = request.session.get('user_name', 'Usuario')
    user_email = request.session.get('user_email', '')
    user_role = request.session.get('user_role', 'estudiante')
    username = request.session.get('username', '')
    numero_cuenta = request.session.get('numero_cuenta', '')
    
    context = {
        'user_name': user_name,
        'user_email': user_email,
        'user_role': user_role,
        'username': username,
        'numero_cuenta': numero_cuenta,
    }
    
    return render(request, 'alumnos/alumnos.html', context)


