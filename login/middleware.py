from django.shortcuts import redirect
from django.urls import reverse

class AuthenticationMiddleware:
    """
    Middleware para verificar autenticación por sesión personalizada.
    Redirige a login si el usuario no está autenticado en rutas protegidas.
    """
    # Rutas que requieren autenticación
    PROTECTED_ROUTES = [
        'alumnos:alumnos',
        'alumnos:',  # Cualquier ruta bajo alumnos
        'profesores:',
        'administradores:',
    ]
    
    # Rutas públicas que NO requieren autenticación
    PUBLIC_ROUTES = [
        'login:login_view',
        'login:register',
        'home:index',
    ]
    
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        # Verificar si la ruta requiere autenticación
        if self._is_protected_route(request):
            # Si no está autenticado, redirigir a login
            if not request.session.get('user_id'):
                return redirect('login:login_view')
        
        response = self.get_response(request)
        return response
    
    def _is_protected_route(self, request):
        """Verifica si la ruta actual requiere autenticación"""
        current_path = request.path
        
        # Si está en rutas públicas, no proteger
        for public_route in self.PUBLIC_ROUTES:
            if public_route.endswith(':'):
                # Ruta con prefijo (ej: 'login:')
                route_prefix = f"/{public_route.split(':')[0]}/"
                if current_path.startswith(route_prefix):
                    return False
            else:
                # Ruta específica
                if current_path == reverse(public_route):
                    return False
        
        # Si está en rutas protegidas, requerir autenticación
        for protected_route in self.PROTECTED_ROUTES:
            if protected_route.endswith(':'):
                # Ruta con prefijo (ej: 'alumnos:')
                route_prefix = f"/{protected_route.split(':')[0]}/"
                if current_path.startswith(route_prefix):
                    return True
        
        return False
