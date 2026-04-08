from django.db import models
from django.contrib.auth.models import AbstractUser

# 1. Definición de la Empresa
class Empresa(models.Model):
    nombre = models.CharField(max_length=100)
    nit = models.CharField(max_length=20, blank=True, null=True)
    # Nuevo campo para el logo
    logo = models.ImageField(upload_to='empresa_logos/', blank=True, null=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nombre

# 2. Usuarios con Roles y asignados a una Empresa
class Usuario(AbstractUser):
    ROLES = (
        ('ADMIN', 'Administrador Global'),
        ('JEFE', 'Jefe de Mantenimiento'),
        ('TECNICO', 'Técnico de Mantenimiento'),
        ('ESTUDIANTE', 'Operador'),
    )
    rol = models.CharField(max_length=20, choices=ROLES, default='ESTUDIANTE')
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE, null=True, blank=True)
    
    # NUEVO CAMPO: Foto de perfil
    foto_perfil = models.ImageField(upload_to='fotos_perfil/', blank=True, null=True)

    def __str__(self):
        return f"{self.username} - {self.rol}"

# 3. Áreas dentro de la Empresa
class Area(models.Model):
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True)

    def __str__(self):
        return f"{self.nombre} ({self.empresa.nombre})"

# 4. Hoja de Vida del Equipo (Activo)
class Equipo(models.Model):
    area = models.ForeignKey(Area, on_delete=models.CASCADE)
    codigo = models.CharField(max_length=50, unique=True)
    nombre = models.CharField(max_length=150)
    marca = models.CharField(max_length=50, blank=True)
    modelo = models.CharField(max_length=50, blank=True)
    numero_serie = models.CharField(max_length=50, blank=True)
    caracteristicas_tecnicas = models.TextField(help_text="Especificaciones, voltaje, RPM, etc.")
    fotografia = models.ImageField(upload_to='equipos_fotos/', blank=True, null=True)
    fecha_adquisicion = models.DateField(blank=True, null=True)
    estado = models.BooleanField(default=True, help_text="True=Activo, False=Inactivo")

    def __str__(self):
        return f"[{self.codigo}] {self.nombre}"

# 5. Planes de Mantenimiento
class PlanMantenimiento(models.Model):
    TIPOS = (
        ('PREVENTIVO', 'Preventivo'),
        ('PREDICTIVO', 'Predictivo'),
        ('CALIBRACION', 'Calibración'),
    )
    equipo = models.ForeignKey(Equipo, on_delete=models.CASCADE)
    nombre_plan = models.CharField(max_length=100)
    tipo = models.CharField(max_length=20, choices=TIPOS)
    frecuencia_dias = models.IntegerField(help_text="Cada cuántos días se debe realizar")
    tareas_a_realizar = models.TextField(help_text="Paso a paso del mantenimiento")

    def __str__(self):
        return f"{self.nombre_plan} - {self.equipo.nombre}"

# 6. Órdenes de Trabajo (Historial y Ejecución)
class OrdenTrabajo(models.Model):
    ESTADOS = (
        ('ABIERTA', 'Abierta'),
        ('EN_PROCESO', 'En Proceso'),
        ('CERRADA', 'Cerrada / Completada'),
    )
    plan = models.ForeignKey(PlanMantenimiento, on_delete=models.SET_NULL, null=True, blank=True)
    equipo = models.ForeignKey(Equipo, on_delete=models.CASCADE)
    creada_por = models.ForeignKey(Usuario, related_name='ordenes_creadas', on_delete=models.SET_NULL, null=True) # Jefe
    asignada_a = models.ForeignKey(Usuario, related_name='ordenes_asignadas', on_delete=models.SET_NULL, null=True) # Técnico
    fecha_programada = models.DateField()
    fecha_ejecucion = models.DateField(null=True, blank=True)
    estado = models.CharField(max_length=20, choices=ESTADOS, default='ABIERTA')
    observaciones = models.TextField(blank=True, help_text="Reporte final del técnico tras la intervención")

    def __str__(self):
        return f"OT-{self.id} | {self.equipo.nombre} | {self.estado}"