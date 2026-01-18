from django.db import models
from django.contrib.auth.hashers import make_password, check_password

class Usuario(models.Model):
    ROLES = [
        ('estudiante', 'Estudiante'),
        ('profesor', 'Profesor'),
        ('administrador', 'Administrador'),
    ]
    
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=70)
    email = models.EmailField(max_length=100, unique=True)
    password_hash = models.CharField(max_length=255)
    rol = models.CharField(max_length=20, choices=ROLES)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    numero_cuenta = models.IntegerField(unique=True, null=True, blank=True)
    perfil_completado = models.BooleanField(default=False)
    telefono = models.CharField(max_length=20, null=True, blank=True)
    usuario = models.CharField(max_length=70)
    
    class Meta:
        db_table = 'usuarios'
    
    def __str__(self):
        return f"{self.nombre} {self.apellido} - {self.email}"
    
    def set_password(self, raw_password):
        self.password_hash = make_password(raw_password)
    
    def check_password(self, raw_password):
        return check_password(raw_password, self.password_hash)

class PerfilEstudiante(models.Model):
    estudiante = models.ForeignKey(Usuario, on_delete=models.CASCADE, limit_choices_to={'rol': 'estudiante'})
    semestre = models.IntegerField()
    facultad = models.CharField(max_length=100)
    carrera = models.CharField(max_length=100)
    estilos_aprendizaje = models.CharField(max_length=255, null=True, blank=True)
    marco_id = models.IntegerField(null=True, blank=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'perfiles_estudiante'
    
    def __str__(self):
        return f"Perfil de {self.estudiante.nombre} - Semestre {self.semestre}"