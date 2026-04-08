from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Empresa, Usuario, Area, Equipo, PlanMantenimiento, OrdenTrabajo

# 1. Creamos una configuración personalizada para el panel de Usuario
class CustomUserAdmin(UserAdmin):
    # Le decimos a Django que agregue nuestra sección al final de las opciones
    fieldsets = UserAdmin.fieldsets + (
        ('Información de Mantenimiento (CMMS)', {'fields': ('rol', 'empresa')}),
    )

# 2. Registramos el usuario usando nuestra configuración personalizada
admin.site.register(Usuario, CustomUserAdmin)

# 3. Registramos el resto de tablas normalmente
admin.site.register(Empresa)
admin.site.register(Area)
admin.site.register(Equipo)
admin.site.register(PlanMantenimiento)
admin.site.register(OrdenTrabajo)