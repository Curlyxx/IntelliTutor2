from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout

from django.db import connection
import hashlib
import secrets
import string

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


def login_view(request):
    if request.session.get('user_id'):
        return redirect('alumnos:alumnos')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        print(f"Intento de login: usuario={username}")  # DEBUG
        
        if not username or not password:
            messages.error(request, 'Por favor ingresa usuario y contraseña')
            return render(request, 'login/login.html')
        
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
                        request.session.modified = True  # Asegurar que se guarde la sesión
                        
                        messages.success(request, f'¡Bienvenido de nuevo, {nombre}!')
                        return redirect('alumnos:alumnos')
                    else:
                        messages.error(request, 'Usuario o contraseña incorrectos')
                else:
                    messages.error(request, 'Usuario o contraseña incorrectos')
                    
        except Exception as e:
            print(f"Error completo: {e}")  # DEBUG
            messages.error(request, 'Error al iniciar sesión. Por favor intenta de nuevo.')
        
        return render(request, 'login/login.html')
    
    return render(request, 'login/login.html')

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
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')
        password_confirm = request.POST.get('password_confirm')
        terms = request.POST.get('terms')
        
        # Validaciones básicas
        if not terms:
            messages.error(request, 'Debes aceptar los términos y condiciones')
            return render(request, 'login/register.html')
        
        if password != password_confirm:
            messages.error(request, 'Las contraseñas no coinciden')
            return render(request, 'login/register.html')
        
        if not all([first_name, last_name, email, username, password]):
            messages.error(request, 'Todos los campos son obligatorios')
            return render(request, 'login/register.html')
        
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
                    return render(request, 'login/register.html')
            
            # Insertar en la base de datos CON NOMBRE Y APELLIDO SEPARADOS
            with connection.cursor() as cursor:
                sql = """
                INSERT INTO usuarios 
                (nombre, apellido, email, password_hash, rol, usuario, perfil_completado, numero_cuenta) 
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                """
                cursor.execute(sql, [
                    first_name,      # nombre (solo el primer nombre)
                    last_name,       # apellido
                    email,
                    password_hash,
                    'estudiante',
                    username,
                    0,
                    numero_cuenta
                ])
            
            messages.success(request, '¡Usuario creado exitosamente!')
            return redirect('login:login_view')
            
        except Exception as e:
            messages.error(request, f'Error al crear la cuenta: {str(e)}')
            return render(request, 'login/register.html')
    
    return render(request, 'login/register.html')