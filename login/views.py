from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.conf import settings
from django.db import connection
from django.http import JsonResponse
import hashlib
import secrets
import string
import requests
import json
import re

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


def verify_recaptcha(recaptcha_response):
    """Verifica el reCAPTCHA con Google"""
    data = {
        'secret': settings.RECAPTCHA_SECRET_KEY,
        'response': recaptcha_response
    }
    response = requests.post('https://www.google.com/recaptcha/api/siteverify', data=data)
    result = response.json()
    return result.get('success', False)

def login_view(request):
    context = {'recaptcha_site_key': settings.RECAPTCHA_SITE_KEY}
    
    if request.session.get('user_id'):
        return redirect('alumnos:alumnos')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        recaptcha_response = request.POST.get('g-recaptcha-response')
        
        # Verificar si es una petición AJAX
        is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
        
        if not username or not password:
            if is_ajax:
                return JsonResponse({'success': False, 'message': 'Por favor ingresa usuario y contraseña'})
            messages.error(request, 'Por favor ingresa usuario y contraseña')
            return render(request, 'login/login.html', context)
        
        if not recaptcha_response or not verify_recaptcha(recaptcha_response):
            if is_ajax:
                return JsonResponse({'success': False, 'message': 'Por favor completa el reCAPTCHA'})
            messages.error(request, 'Por favor completa el reCAPTCHA')
            return render(request, 'login/login.html', context)
        
        try:
            with connection.cursor() as cursor:
                cursor.execute("""
                    SELECT id, nombre, apellido, email, password_hash, rol, usuario, numero_cuenta 
                    FROM usuarios 
                    WHERE usuario = %s OR email = %s
                """, [username, username])
                
                user_data = cursor.fetchone()
                
                if user_data:
                    user_id, nombre, apellido, email, password_hash, rol, usuario, numero_cuenta = user_data
                    
                    # Verificar contraseña
                    password_correcta = verificar_password(password, password_hash)
                    
                    if password_correcta:
                        request.session['user_id'] = user_id
                        request.session['user_name'] = f"{nombre} {apellido}"
                        request.session['user_email'] = email
                        request.session['user_role'] = rol
                        request.session['username'] = usuario
                        request.session['numero_cuenta'] = numero_cuenta
                        request.session['is_authenticated'] = True
                        request.session.modified = True
                        
                        # Redirigir según el rol
                        if rol == 'estudiante':
                            redirect_url = '/alumnos/'
                            redirect_name = 'alumnos:alumnos'
                        elif rol == 'profesor':
                            redirect_url = '/profesores/'
                            redirect_name = 'profesores:profesores'
                        elif rol == 'administrador':
                            redirect_url = '/administradores/'
                            redirect_name = 'administradores:admin'
                        else:
                            redirect_url = '/alumnos/'
                            redirect_name = 'alumnos:alumnos'
                        
                        if is_ajax:
                            return JsonResponse({'success': True, 'message': f'¡Bienvenido de nuevo, {nombre}!', 'redirect': redirect_url})
                        messages.success(request, f'¡Bienvenido de nuevo, {nombre}!')
                        return redirect(redirect_name)
                    else:
                        if is_ajax:
                            return JsonResponse({'success': False, 'message': 'Usuario o contraseña incorrectos'})
                        messages.error(request, 'Usuario o contraseña incorrectos')
                else:
                    if is_ajax:
                        return JsonResponse({'success': False, 'message': 'Usuario o contraseña incorrectos'})
                    messages.error(request, 'Usuario o contraseña incorrectos')
                    
        except Exception as e:
            print(f"Error completo: {e}")
            if is_ajax:
                return JsonResponse({'success': False, 'message': 'Error al iniciar sesión. Por favor intenta de nuevo.'})
            messages.error(request, 'Error al iniciar sesión. Por favor intenta de nuevo.')
        
        return render(request, 'login/login.html', context)
    
    return render(request, 'login/login.html', context)

def logout_view(request):
    # Limpiar claves de sesión personalizadas
    for key in ['user_id', 'user_name', 'user_email', 'user_role', 'username', 'numero_cuenta', 'is_authenticated']:
        if key in request.session:
            try:
                del request.session[key]
            except KeyError:
                pass
    request.session.modified = True

    # Cerrar sesión de Django (por si se registró con auth)
    auth_logout(request)
    messages.success(request, 'Sesión cerrada correctamente')
    return redirect('home:index')

def register(request):
    if request.method == 'POST':
        # Obtener datos del formulario
        first_name = request.POST.get('first_name', '').strip()
        last_name = request.POST.get('last_name', '').strip()
        email = request.POST.get('email', '').strip()
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password')
        password_confirm = request.POST.get('password_confirm')
        telefono = request.POST.get('telefono', '').strip()
        terms = request.POST.get('terms')
        
        # Crear contexto con los datos del formulario
        context = {
            'first_name': first_name,
            'last_name': last_name,
            'email': email,
            'username': username,
            'telefono': telefono,
        }
        
        # Validaciones básicas
        if not terms:
            messages.error(request, 'Debes aceptar los términos y condiciones')
            return render(request, 'login/register.html', context)
        
        if not all([first_name, last_name, email, username, password, telefono]):
            messages.error(request, 'Todos los campos son obligatorios')
            return render(request, 'login/register.html', context)
        
        # Validaciones de formato
        if len(first_name) > 100 or not re.match(r'^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s]+$', first_name):
            messages.error(request, 'Nombre inválido: solo letras, acentos, ñ y espacios (máx. 100 caracteres)')
            return render(request, 'login/register.html', context)
        
        if len(last_name) > 70 or not re.match(r'^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s]+$', last_name):
            messages.error(request, 'Apellido inválido: solo letras, acentos, ñ y espacios (máx. 70 caracteres)')
            return render(request, 'login/register.html', context)
        
        if len(username) > 50:
            messages.error(request, 'Usuario muy largo (máx. 50 caracteres)')
            return render(request, 'login/register.html', context)
        
        if not re.match(r'^[0-9]{10}$', telefono):
            messages.error(request, 'Teléfono inválido: exactamente 10 dígitos')
            return render(request, 'login/register.html', context)
        
        if password != password_confirm:
            messages.error(request, 'Las contraseñas no coinciden')
            return render(request, 'login/register.html', context)
        
        try:
            # Generar número de cuenta único (9 dígitos)
            def generar_numero_cuenta():
                while True:
                    numero = ''.join(secrets.choice(string.digits[1:]) + 
                                   ''.join(secrets.choice(string.digits) for _ in range(8)))
                    
                    with connection.cursor() as cursor:
                        cursor.execute("SELECT id FROM usuarios WHERE numero_cuenta = %s", [numero])
                        if not cursor.fetchone():
                            return int(numero)
            
            numero_cuenta = generar_numero_cuenta()
            
            # Crear hash de la contraseña usando scrypt
            def generar_hash_scrypt(password):
                salt = secrets.token_hex(16)
                
                password_hash = hashlib.scrypt(
                    password.encode('utf-8'),
                    salt=salt.encode('utf-8'),
                    n=16384,
                    r=8,
                    p=1,
                    dklen=64
                )
                
                hash_hex = password_hash.hex()
                return f"scrypt:16384:8:1${salt}${hash_hex}"
            
            password_hash = generar_hash_scrypt(password)
            
            # Verificar si el usuario o email ya existen
            with connection.cursor() as cursor:
                cursor.execute("SELECT id FROM usuarios WHERE email = %s OR usuario = %s", [email, username])
                if cursor.fetchone():
                    messages.error(request, 'El correo electrónico o nombre de usuario ya está registrado')
                    return render(request, 'login/register.html', context)
            
            # Insertar en la base de datos CON NOMBRE Y APELLIDO SEPARADOS
            with connection.cursor() as cursor:
                sql = """
                INSERT INTO usuarios 
                (nombre, apellido, email, password_hash, rol, usuario, perfil_completado, numero_cuenta, telefono) 
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                """
                cursor.execute(sql, [
                    first_name,      # nombre (solo el primer nombre)
                    last_name,       # apellido
                    email,
                    password_hash,
                    'estudiante',
                    username,
                    0,
                    numero_cuenta,
                    telefono
                ])
            
            messages.success(request, '¡Usuario creado exitosamente!')
            return redirect('login:login_view')
            
        except Exception as e:
            messages.error(request, f'Error al crear la cuenta: {str(e)}')
            return render(request, 'login/register.html', context)
    
    return render(request, 'login/register.html')