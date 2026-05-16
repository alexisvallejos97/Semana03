from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.utils import timezone
from clientes.models import Cliente
from rutas.models import Ruta
from envios.models import Empleado, Encomienda, HistorialEstado
from config.choices import EstadoGeneral, EstadoEnvio, TipoDocumento
import uuid

class Command(BaseCommand):
    help = 'Crea datos de ejemplo para el sistema Laudesciende'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS('Iniciando carga de datos de ejemplo...'))

        if User.objects.filter(username='admin').exists():
            self.stdout.write('El superusuario admin ya existe, saltando...')
        else:
            User.objects.create_superuser('admin', 'admin@laudesciende.com', 'admin123')
            self.stdout.write(self.style.SUCCESS('Superusuario creado: admin / admin123'))

        User.objects.get_or_create(username='operador1', defaults={'email': 'operador1@laudesciende.com', 'password': 'operador123'})
        User.objects.get_or_create(username='operador2', defaults={'email': 'operador2@laudesciende.com', 'password': 'operador123'})

        clientes_data = [
            {'tipo_doc': TipoDocumento.DNI, 'nro_doc': '72345678', 'nombres': 'Carlos', 'apellidos': 'Garcia Lopez', 'telefono': '987654321', 'email': 'carlos@email.com', 'direccion': 'Av. Lima 123'},
            {'tipo_doc': TipoDocumento.DNI, 'nro_doc': '73456789', 'nombres': 'Maria', 'apellidos': 'Rodriguez Perez', 'telefono': '987654322', 'email': 'maria@email.com', 'direccion': 'Jr. Arequipa 456'},
            {'tipo_doc': TipoDocumento.DNI, 'nro_doc': '74567890', 'nombres': 'Jose', 'apellidos': 'Martinez Ruiz', 'telefono': '987654323', 'email': 'jose@email.com', 'direccion': 'Calle Cusco 789'},
            {'tipo_doc': TipoDocumento.RUC, 'nro_doc': '20123456789', 'nombres': 'Empresa', 'apellidos': 'SAC', 'telefono': '987654324', 'email': 'empresa@email.com', 'direccion': 'Av. Javier Prado 1000'},
            {'tipo_doc': TipoDocumento.DNI, 'nro_doc': '75678901', 'nombres': 'Ana', 'apellidos': 'Sanchez Torres', 'telefono': '987654325', 'email': 'ana@email.com', 'direccion': 'Av. Brasil 200'},
            {'tipo_doc': TipoDocumento.DNI, 'nro_doc': '76789012', 'nombres': 'Luis', 'apellidos': 'Diaz Morales', 'telefono': '987654326', 'email': 'luis@email.com', 'direccion': 'Jr. Puno 300'},
            {'tipo_doc': TipoDocumento.DNI, 'nro_doc': '77890123', 'nombres': 'Rosa', 'apellidos': 'Flores Vargas', 'telefono': '987654327', 'email': 'rosa@email.com', 'direccion': 'Av. Tacna 400'},
            {'tipo_doc': TipoDocumento.DNI, 'nro_doc': '78901234', 'nombres': 'Pedro', 'apellidos': 'Castro Ramos', 'telefono': '987654328', 'email': 'pedro@email.com', 'direccion': 'Calle Piura 500'},
        ]

        clientes = []
        for data in clientes_data:
            cliente, created = Cliente.objects.get_or_create(nro_doc=data['nro_doc'], defaults=data)
            if created:
                clientes.append(cliente)
        self.stdout.write(self.style.SUCCESS(f'{len(clientes)} clientes creados'))

        rutas_data = [
            {'codigo': 'R001', 'origen': 'Lima', 'destino': 'Arequipa', 'descripcion': 'Ruta principal sur', 'precio_base': 25.00, 'dias_entrega': 2},
            {'codigo': 'R002', 'origen': 'Lima', 'destino': 'Trujillo', 'descripcion': 'Ruta norte costa', 'precio_base': 20.00, 'dias_entrega': 1},
            {'codigo': 'R003', 'origen': 'Lima', 'destino': 'Cusco', 'descripcion': 'Ruta sur sierra', 'precio_base': 35.00, 'dias_entrega': 3},
            {'codigo': 'R004', 'origen': 'Arequipa', 'destino': 'Puno', 'descripcion': 'Ruta altiplano', 'precio_base': 15.00, 'dias_entrega': 1},
            {'codigo': 'R005', 'origen': 'Trujillo', 'destino': 'Chiclayo', 'descripcion': 'Ruta norte intermedia', 'precio_base': 12.00, 'dias_entrega': 1},
        ]

        rutas = []
        for data in rutas_data:
            ruta, created = Ruta.objects.get_or_create(codigo=data['codigo'], defaults=data)
            if created:
                rutas.append(ruta)
        self.stdout.write(self.style.SUCCESS(f'{len(rutas)} rutas creadas'))

        empleados_data = [
            {'codigo': 'EMP001', 'nombres': 'Juan', 'apellidos': 'Perez Gomez', 'cargo': 'Operador Logístico', 'email': 'operador1@laudesciende.com', 'telefono': '999888777', 'fecha_ingreso': '2024-01-15'},
            {'codigo': 'EMP002', 'nombres': 'Sofia', 'apellidos': 'Lopez Mendoza', 'cargo': 'Coordinadora de Envíos', 'email': 'operador2@laudesciende.com', 'telefono': '999888778', 'fecha_ingreso': '2024-03-20'},
            {'codigo': 'EMP003', 'nombres': 'Diego', 'apellidos': 'Torres Silva', 'cargo': 'Almacenista', 'email': 'diego@laudesciende.com', 'telefono': '999888779', 'fecha_ingreso': '2024-06-10'},
        ]

        empleados = []
        for data in empleados_data:
            emp, created = Empleado.objects.get_or_create(codigo=data['codigo'], defaults=data)
            if created:
                empleados.append(emp)
        self.stdout.write(self.style.SUCCESS(f'{len(empleados)} empleados creados'))

        encomiendas_data = [
            {'descripcion': 'Paquete con documentos importantes', 'peso_kg': 2.5, 'remitente': 0, 'destinatario': 1, 'ruta': 0, 'estado': EstadoEnvio.PENDIENTE},
            {'descripcion': 'Caja con productos electrónicos', 'peso_kg': 8.0, 'remitente': 2, 'destinatario': 3, 'ruta': 1, 'estado': EstadoEnvio.EN_TRANSITO},
            {'descripcion': 'Sobres con facturas', 'peso_kg': 1.0, 'remitente': 4, 'destinatario': 5, 'ruta': 2, 'estado': EstadoEnvio.EN_DESTINO},
            {'descripcion': 'Paquete de ropa', 'peso_kg': 3.5, 'remitente': 6, 'destinatario': 7, 'ruta': 0, 'estado': EstadoEnvio.ENTREGADO},
            {'descripcion': 'Caja con herramientas', 'peso_kg': 12.0, 'remitente': 1, 'destinatario': 2, 'ruta': 3, 'estado': EstadoEnvio.PENDIENTE},
            {'descripcion': 'Documentos legales', 'peso_kg': 0.5, 'remitente': 3, 'destinatario': 4, 'ruta': 4, 'estado': EstadoEnvio.EN_TRANSITO},
            {'descripcion': 'Equipos de computo', 'peso_kg': 15.0, 'remitente': 5, 'destinatario': 6, 'ruta': 0, 'estado': EstadoEnvio.ENTREGADO},
            {'descripcion': 'Muestras de laboratorio', 'peso_kg': 4.0, 'remitente': 7, 'destinatario': 0, 'ruta': 1, 'estado': EstadoEnvio.PENDIENTE},
            {'descripcion': 'Libros y materiales educativos', 'peso_kg': 6.5, 'remitente': 0, 'destinatario': 3, 'ruta': 2, 'estado': EstadoEnvio.EN_TRANSITO},
            {'descripcion': 'Repuestos automotrices', 'peso_kg': 20.0, 'remitente': 2, 'destinatario': 5, 'ruta': 3, 'estado': EstadoEnvio.ENTREGADO},
            {'descripcion': 'Productos agrícolas', 'peso_kg': 10.0, 'remitente': 4, 'destinatario': 7, 'ruta': 4, 'estado': EstadoEnvio.PENDIENTE},
            {'descripcion': 'Material de oficina', 'peso_kg': 5.0, 'remitente': 6, 'destinatario': 1, 'ruta': 0, 'estado': EstadoEnvio.EN_DESTINO},
            {'descripcion': 'Artículos deportivos', 'peso_kg': 7.5, 'remitente': 1, 'destinatario': 4, 'ruta': 1, 'estado': EstadoEnvio.ENTREGADO},
            {'descripcion': 'Medicamentos', 'peso_kg': 2.0, 'remitente': 3, 'destinatario': 6, 'ruta': 2, 'estado': EstadoEnvio.EN_TRANSITO},
            {'descripcion': 'Juguetes', 'peso_kg': 4.5, 'remitente': 5, 'destinatario': 2, 'ruta': 3, 'estado': EstadoEnvio.PENDIENTE},
        ]

        hoy = timezone.now()
        encomiendas = []
        for i, data in enumerate(encomiendas_data):
            ruta = rutas[data.pop('ruta')]
            remitente = clientes[data.pop('remitente')]
            destinatario = clientes[data.pop('destinatario')]
            estado = data.pop('estado')
            empleado = empleados[i % len(empleados)]

            codigo = f"ENC-{hoy.strftime('%Y%m%d')}-{str(uuid.uuid4())[:6].upper()}"
            peso = data['peso_kg']
            peso_excedente = max(0, float(peso) - 5.0)
            costo = float(ruta.precio_base) + (peso_excedente * 2.50)
            fecha_est = hoy.date() + timezone.timedelta(days=ruta.dias_entrega)

            enc = Encomienda.objects.create(
                codigo=codigo,
                ruta=ruta,
                remitente=remitente,
                destinatario=destinatario,
                empleado_registro=empleado,
                estado=estado,
                costo_envio=costo,
                fecha_entrega_est=fecha_est,
                **data
            )
            encomiendas.append(enc)

        self.stdout.write(self.style.SUCCESS(f'{len(encomiendas)} encomiendas creadas'))

        historial_count = 0
        for enc in encomiendas:
            if enc.estado in [EstadoEnvio.EN_TRANSITO, EstadoEnvio.EN_DESTINO, EstadoEnvio.ENTREGADO]:
                HistorialEstado.objects.create(
                    encomienda=enc,
                    estado_anterior=EstadoEnvio.PENDIENTE,
                    estado_nuevo=EstadoEnvio.EN_TRANSITO,
                    observacion='Encomienda recogida y en camino',
                    empleado=enc.empleado_registro
                )
                historial_count += 1
            if enc.estado in [EstadoEnvio.EN_DESTINO, EstadoEnvio.ENTREGADO]:
                HistorialEstado.objects.create(
                    encomienda=enc,
                    estado_anterior=EstadoEnvio.EN_TRANSITO,
                    estado_nuevo=EstadoEnvio.EN_DESTINO,
                    observacion='Llegó a ciudad de destino',
                    empleado=enc.empleado_registro
                )
                historial_count += 1
            if enc.estado == EstadoEnvio.ENTREGADO:
                enc.fecha_entrega_real = hoy.date() - timezone.timedelta(days=1)
                enc.save()
                HistorialEstado.objects.create(
                    encomienda=enc,
                    estado_anterior=EstadoEnvio.EN_DESTINO,
                    estado_nuevo=EstadoEnvio.ENTREGADO,
                    observacion='Entregado al destinatario',
                    empleado=enc.empleado_registro
                )
                historial_count += 1

        self.stdout.write(self.style.SUCCESS(f'{historial_count} registros de historial creados'))
        self.stdout.write(self.style.SUCCESS('\nDatos de ejemplo cargados exitosamente!'))
        self.stdout.write(self.style.WARNING('\nUsuarios de prueba:'))
        self.stdout.write('  Admin: admin / admin123')
        self.stdout.write('  Operador 1: operador1 / operador123')
        self.stdout.write('  Operador 2: operador2 / operador123')
