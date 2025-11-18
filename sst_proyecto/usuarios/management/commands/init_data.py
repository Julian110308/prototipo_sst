from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

# Importar modelos
try:
    from emergencias.models import TipoEmergencia, ContactoExterno
    from control_acceso.models import ConfiguracionAforo, Geocerca
    from mapas.models import EdificioBloque, PuntoEncuentro
except ImportError as e:
    print(f"Error importando modelos: {e}")

User = get_user_model()

class Command(BaseCommand):
    help = 'Inicializa datos de prueba para el sistema SST'
    
    def handle(self, *args, **options):
        self.stdout.write('🚀 Inicializando datos del Sistema SST...')
        
        try:
            # 1. CREAR TIPOS DE EMERGENCIA
            self.crear_tipos_emergencia()
            
            # 2. CREAR CONTACTOS EXTERNOS
            self.crear_contactos_externos()
            
            # 3. CONFIGURAR AFORO (VERSIÓN SEGURA)
            self.configurar_aforo_seguro()
            
            # 4. CREAR GEOCERCA
            self.crear_geocerca()
            
            self.stdout.write(
                self.style.SUCCESS('✅ Datos iniciales creados exitosamente!')
            )
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'❌ Error: {e}')
            )
    
    def crear_tipos_emergencia(self):
        """Crear tipos de emergencia predefinidos"""
        self.stdout.write('📋 Creando tipos de emergencia...')
        
        tipos = [
            {
                'nombre': 'Incendio',
                'descripcion': 'Fuego o incendio en instalaciones',
                'prioridad': 1,
                'color': '#FF0000',
                'protocolo': 'Activar alarma, evacuar el área, usar extintores, llamar bomberos'
            },
            {
                'nombre': 'Accidente Médico',
                'descripcion': 'Emergencia médica o de salud',
                'prioridad': 1,
                'color': '#FF4500',
                'protocolo': 'Primeros auxilios, llamar ambulancia, aislar al afectado'
            },
            {
                'nombre': 'Fuga de Gas',
                'descripcion': 'Fuga de gas o sustancias peligrosas',
                'prioridad': 1,
                'color': '#FFA500',
                'protocolo': 'Evacuar área, cortar suministro eléctrico, ventilar'
            }
        ]
        
        for tipo_data in tipos:
            tipo, created = TipoEmergencia.objects.get_or_create(
                nombre=tipo_data['nombre'],
                defaults=tipo_data
            )
            if created:
                self.stdout.write(f'  ✅ Tipo emergencia: {tipo.nombre}')
    
    def crear_contactos_externos(self):
        """Crear contactos de emergencia externos"""
        self.stdout.write('📞 Creando contactos externos...')
        
        contactos = [
            {
                'nombre': 'Bomberos Sogamoso',
                'entidad': 'Cuerpo de Bomberos Voluntarios',
                'tipo': 'BOMBEROS',
                'telefono_principal': '6067701122',
                'orden_contacto': 1
            },
            {
                'nombre': 'Ambulancia CRUZ ROJA',
                'entidad': 'Cruz Roja Colombiana',
                'tipo': 'AMBULANCIA',
                'telefono_principal': '6067701144',
                'orden_contacto': 2
            }
        ]
        
        for contacto_data in contactos:
            contacto, created = ContactoExterno.objects.get_or_create(
                nombre=contacto_data['nombre'],
                defaults=contacto_data
            )
            if created:
                self.stdout.write(f'  ✅ Contacto: {contacto.nombre}')
    
    def configurar_aforo_seguro(self):
        """Configurar aforo de manera segura"""
        self.stdout.write('👥 Configurando aforo...')
        
        try:
            # Verificar si ya existe
            if ConfiguracionAforo.objects.exists():
                config = ConfiguracionAforo.objects.first()
                self.stdout.write(f'  ✅ Configuración aforo ya existe')
                return
            
            # Crear con campos básicos que SÍ existen
            config_data = {'aforo_maximo': 2000}
            
            # Solo agregar aforo_alerta si el campo existe
            if hasattr(ConfiguracionAforo, 'aforo_alerta'):
                config_data['aforo_alerta'] = 1800
            
            config = ConfiguracionAforo.objects.create(**config_data)
            self.stdout.write(f'  ✅ Configuración aforo creada: {config.aforo_maximo} personas')
            
        except Exception as e:
            self.stdout.write(f'  ⚠️  Error configurando aforo: {e}')
    
    def crear_geocerca(self):
        """Crear geocerca del centro minero"""
        self.stdout.write('🗺️ Creando geocerca...')
        
        try:
            geocerca, created = Geocerca.objects.get_or_create(
                nombre="Centro Minero SENA Boyacá",
                defaults={
                    'centro_latitud': 5.5339,
                    'centro_longitud': -73.3674,
                    'radio_metros': 200
                }
            )
            if created:
                self.stdout.write(f'  ✅ Geocerca: {geocerca.nombre}')
            else:
                self.stdout.write(f'  ✅ Geocerca ya existe')
                
        except Exception as e:
            self.stdout.write(f'  ⚠️  Error creando geocerca: {e}')