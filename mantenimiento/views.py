from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Equipo, OrdenTrabajo

@login_required(login_url='login') # Obliga a iniciar sesión para ver esto
def dashboard(request):
    usuario = request.user
    
    # Filtramos datos según la empresa a la que pertenece el usuario
    if usuario.empresa:
        equipos_totales = Equipo.objects.filter(area__empresa=usuario.empresa).count()
        ordenes_abiertas = OrdenTrabajo.objects.filter(equipo__area__empresa=usuario.empresa, estado='ABIERTA').count()
    else:
        equipos_totales = 0
        ordenes_abiertas = 0

    contexto = {
        'equipos_totales': equipos_totales,
        'ordenes_abiertas': ordenes_abiertas,
    }
    
    return render(request, 'mantenimiento/dashboard.html', contexto)