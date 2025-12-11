"""
URL configuration for sst_proyecto project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import views as auth_views
from django.urls import path, include
from django.views.generic import TemplateView   # 👉 AGREGADO
from usuarios.views import registro_view, perfil_view
from control_acceso.models import RegistroAcceso, ConfiguracionAforo
from emergencias.models import Emergencia
from django.utils import timezone
from datetime import timedelta


# Vistas para usuarios autenticados (usan base.html)
@login_required
def dashboard_view(request):
    # Obtener datos para el dashboard
    ahora = timezone.now()
    hoy = ahora.date()
    ayer = hoy - timedelta(days=1)

    # Personas en centro (ingresos sin egreso)
    personas_en_centro = RegistroAcceso.objects.filter(
        fecha_hora_egreso__isnull=True,
        tipo='INGRESO'
    ).count()

    # Ingresos hoy
    ingresos_hoy = RegistroAcceso.objects.filter(
        fecha_hora_ingreso__date=hoy,
        tipo='INGRESO'
    ).count()

    # Ingresos ayer para comparación
    ingresos_ayer = RegistroAcceso.objects.filter(
        fecha_hora_ingreso__date=ayer,
        tipo='INGRESO'
    ).count()

    # Calcular porcentaje de cambio
    if ingresos_ayer > 0:
        cambio_ingresos = ((ingresos_hoy - ingresos_ayer) / ingresos_ayer) * 100
    else:
        cambio_ingresos = 0

    # Emergencias activas (no resueltas)
    emergencias_activas = Emergencia.objects.filter(
        estado__in=['REPORTADA', 'EN_ATENCION']
    ).count()

    # Configuración de aforo
    try:
        config_aforo = ConfiguracionAforo.objects.filter(activo=True).first()
        aforo_maximo = config_aforo.aforo_maximo if config_aforo else 2000
    except:
        aforo_maximo = 2000

    # Calcular capacidad actual
    capacidad_porcentaje = (personas_en_centro / aforo_maximo) * 100 if aforo_maximo > 0 else 0

    # Últimas emergencias
    ultimas_emergencias = Emergencia.objects.select_related('tipo', 'reportada_por').order_by('-fecha_hora_reporte')[:5]

    context = {
        'personas_en_centro': personas_en_centro,
        'ingresos_hoy': ingresos_hoy,
        'cambio_ingresos': cambio_ingresos,
        'emergencias_activas': emergencias_activas,
        'capacidad_porcentaje': capacidad_porcentaje,
        'aforo_maximo': aforo_maximo,
        'ultimas_emergencias': ultimas_emergencias,
    }

    return render(request, 'dashboard.html', context)

@login_required
def control_acceso_view(request):
    return render(request, 'control_acceso.html')

@login_required
def mapas_view(request):
    return render(request, 'mapas.html')

@login_required
def emergencias_view(request):
    return render(request, 'emergencias.html')

@login_required
def reportes_view(request):
    return render(request, 'reportes.html')


urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Login
    path('accounts/login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('accounts/profile/', perfil_view, name='profile'),

    # 👉👉 NUEVO: página inicial será el registro (registro.html)
    path('', registro_view, name='registro'),

    # 👉 Dashboard ahora tiene su propia URL
    path('dashboard/', dashboard_view, name='dashboard'),

    # Módulos
    path('acceso/', control_acceso_view, name='control_acceso'),
    path('mapas/', mapas_view, name='mapas'),
    path('emergencias/', emergencias_view, name='emergencias'),
    path('reportes/', reportes_view, name='reportes'),
    
    # APIa lo 
    path('api/auth/', include('usuarios.urls')),
    path('api/acceso/', include('control_acceso.urls')),
    path('api/mapas/', include('mapas.urls')),
    path('api/emergencias/', include('emergencias.urls')),
    path('api/reportes/', include('reportes.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
