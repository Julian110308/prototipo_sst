// Funcionalidades básicas del sistema SST

document.addEventListener('DOMContentLoaded', function() {
    // Botón de emergencia
    const botonPanico = document.getElementById('botonPanico');
    if (botonPanico) {
        botonPanico.addEventListener('click', function() {
            if (confirm('¿Está seguro de activar la alerta de emergencia?')) {
                alert('Alerta de emergencia activada. El personal de respuesta está siendo notificado.');
                // Aquí iría la llamada a la API
            }
        });
    }

    // Cargar datos del dashboard
    cargarDatosDashboard();
});

async function cargarDatosDashboard() {
    try {
        const response = await fetch('/api/reportes/dashboard/');
        if (response.ok) {
            const data = await response.json();
            
            // Actualizar métricas
            document.getElementById('personasCentro').textContent = data.personas_en_centro || '0';
            document.getElementById('ingresosHoy').textContent = data.ingresos_hoy || '0';
            document.getElementById('emergenciasActivas').textContent = data.emergencias_activas || '0';
            document.getElementById('porcentajeAforo').textContent = data.porcentaje_aforo ? data.porcentaje_aforo.toFixed(1) + '%' : '0%';
        }
    } catch (error) {
        console.log('Error cargando datos:', error);
    }
}