# 🎓 IntelliTutor2 - Proyecto Django

Este proyecto está desarrollado con el framework **Django** y utiliza **MySQL** como base de datos mediante **phpMyAdmin**.  
Permite ejecutar el sistema de forma local con base de datos incluida.

---

## ✅ Requisitos previos

Asegúrate de tener instalado en tu equipo:

- Python **3.13**
- Git
- MySQL (por ejemplo usando XAMPP)


---

## 📥 Clonar el repositorio

Clona el proyecto desde GitHub:

```bash
git clone https://github.com/Curlyxx/IntelliTutor2.git
cd IntelliTutor2


## Entorno virtual

python -m venv venv

o

venv\Scripts\activate


## Instalar dependencias

## Instala las librerías necesarias:

pip install -r requirements.txt


# Abre phpMyAdmin

# Desde tu navegador:

http://localhost/phpmyadmin


# Crea la base de datos

# Crea una base con el siguiente nombre:

generador_practicas


# Importa la base de datos del proyecto

# Selecciona la base generador_practicas

# Ve a la pestaña Importar

# Selecciona el archivo:

generador_practicas.sql


# Ejecutar el proyecto

# Inicia el servidor local:

python manage.py runserver

