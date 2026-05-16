import uuid
from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError
from config.choices import EstadoGeneral, EstadoEnvio
from envios.validators import peso_positivo, codigo_encomienda
from envios.querysets import EncomiendaQuerySet
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

class Empleado(models.Model):
    codigo = models.CharField(max_length=10, unique=True, verbose_name='Código')
    nombres = models.CharField(max_length=100, verbose_name='Nombres')
    apellidos = models.CharField(max_length=100, verbose_name='Apellidos')
    cargo = models.CharField(max_length=80, verbose_name='Cargo')
    email = models.EmailField(unique=True, verbose_name='Email')
    telefono = models.CharField(max_length=15, blank=True, null=True, verbose_name='Teléfono')
    estado = models.IntegerField(choices=EstadoGeneral.choices, default=EstadoGeneral.ACTIVO, verbose_name='Estado')
    fecha_ingreso = models.DateField(verbose_name='Fecha de Ingreso')
    rutas_asignadas = models.ManyToManyField('rutas.Ruta', related_name='empleados_asignados', blank=True, verbose_name='Rutas Asignadas')

    class Meta:
        verbose_name = 'Empleado'
        verbose_name_plural = 'Empleados'
        ordering = ['apellidos', 'nombres']

    def __str__(self):
        return f"{self.nombres} {self.apellidos} - {self.cargo}"

class Encomienda(models.Model):
    codigo = models.CharField(max_length=20, unique=True, validators=[codigo_encomienda], verbose_name='Código')
    descripcion = models.TextField(verbose_name='Descripción')
    peso_kg = models.DecimalField(max_digits=8, decimal_places=2, validators=[peso_positivo], verbose_name='Peso (kg)')
    volumen_cm3 = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True, verbose_name='Volumen (cm³)')
    remitente = models.ForeignKey('clientes.Cliente', on_delete=models.PROTECT, related_name='envios_como_remitente', verbose_name='Remitente')
    destinatario = models.ForeignKey('clientes.Cliente', on_delete=models.PROTECT, related_name='envios_como_destinatario', verbose_name='Destinatario')
    ruta = models.ForeignKey('rutas.Ruta', on_delete=models.PROTECT, related_name='encomiendas', verbose_name='Ruta')
    empleado_registro = models.ForeignKey('envios.Empleado', on_delete=models.PROTECT, related_name='encomiendas_registradas', verbose_name='Empleado que Registra')
    estado = models.CharField(max_length=2, choices=EstadoEnvio.choices, default=EstadoEnvio.PENDIENTE, verbose_name='Estado')
    costo_envio = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Costo de Envío')
    fecha_registro = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de Registro')
    fecha_entrega_est = models.DateField(blank=True, null=True, verbose_name='Fecha Estimada de Entrega')
    fecha_entrega_real = models.DateField(blank=True, null=True, verbose_name='Fecha Real de Entrega')
    observaciones = models.TextField(blank=True, null=True, verbose_name='Observaciones')

    objects = EncomiendaQuerySet.as_manager()

    class Meta:
        verbose_name = 'Encomienda'
        verbose_name_plural = 'Encomiendas'
        ordering = ['-fecha_registro']

    def __str__(self):
        return f"{self.codigo} - {self.estado}"

    @property
    def esta_entregada(self):
        return self.estado == EstadoEnvio.ENTREGADO

    @property
    def esta_en_transito(self):
        return self.estado in [EstadoEnvio.EN_TRANSITO, EstadoEnvio.EN_DESTINO]

    @property
    def dias_en_transito(self):
        if self.fecha_registro:
            return (timezone.now().date() - self.fecha_registro.date()).days
        return 0

    @property
    def tiene_retraso(self):
        if self.fecha_entrega_est and not self.esta_entregada:
            return timezone.now().date() > self.fecha_entrega_est
        return False

    @property
    def descripcion_corta(self):
        return self.descripcion[:50] + '...' if len(self.descripcion) > 50 else self.descripcion

    def cambiar_estado(self, nuevo_estado, empleado, observacion=''):
        estado_anterior = self.estado
        self.estado = nuevo_estado
        if nuevo_estado == EstadoEnvio.ENTREGADO:
            self.fecha_entrega_real = timezone.now().date()
        self.save()

        HistorialEstado.objects.create(
            encomienda=self,
            estado_anterior=estado_anterior,
            estado_nuevo=nuevo_estado,
            observacion=observacion,
            empleado=empleado
        )

        self._notificar_websocket(estado_anterior, nuevo_estado, observacion, empleado)

    def _notificar_websocket(self, estado_anterior, estado_nuevo, observacion, empleado):
        channel_layer = get_channel_layer()
        estado_display = EstadoEnvio(estado_nuevo).label
        mensaje = {
            'type': 'envio.actualizacion',
            'encomienda_id': self.pk,
            'codigo': self.codigo,
            'estado_anterior': EstadoEnvio(estado_anterior).label,
            'estado_nuevo': estado_display,
            'observacion': observacion,
            'empleado': f"{empleado.nombres} {empleado.apellidos}",
            'fecha': timezone.now().isoformat(),
        }
        async_to_sync(channel_layer.group_send)('encomiendas_global', mensaje)
        async_to_sync(channel_layer.group_send)(f'encomienda_{self.pk}', mensaje)
        async_to_sync(channel_layer.group_send)('dashboard', {
            'type': 'dashboard.actualizacion',
            'accion': 'cambio_estado',
            'encomienda_id': self.pk,
            'codigo': self.codigo,
            'estado_nuevo': estado_nuevo,
        })

    def calcular_costo(self):
        peso_excedente = max(0, float(self.peso_kg) - 5.0)
        return float(self.ruta.precio_base) + (peso_excedente * 2.50)

    @classmethod
    def crear_con_costo_calculado(cls, **kwargs):
        hoy = timezone.now()
        codigo = f"ENC-{hoy.strftime('%Y%m%d')}-{str(uuid.uuid4())[:6].upper()}"
        kwargs['codigo'] = codigo
        ruta = kwargs.get('ruta')
        if ruta:
            kwargs['fecha_entrega_est'] = hoy.date() + timezone.timedelta(days=ruta.dias_entrega)
        encomienda = cls(**kwargs)
        encomienda.costo_envio = encomienda.calcular_costo()
        encomienda.full_clean()
        encomienda.save()
        return encomienda

    def clean(self):
        super().clean()
        if self.remitente and self.destinatario and self.remitente == self.destinatario:
            raise ValidationError({'destinatario': 'El remitente y destinatario no pueden ser la misma persona.'})
        if self.fecha_entrega_est and self.fecha_entrega_est < timezone.now().date() and not self.pk:
            raise ValidationError({'fecha_entrega_est': 'La fecha estimada no puede ser en el pasado.'})
        if self.fecha_entrega_real and self.fecha_entrega_est and self.fecha_entrega_real < self.fecha_entrega_est:
            raise ValidationError({'fecha_entrega_real': 'La fecha real no puede ser anterior a la estimada.'})

class HistorialEstado(models.Model):
    encomienda = models.ForeignKey(Encomienda, on_delete=models.CASCADE, related_name='historial', verbose_name='Encomienda')
    estado_anterior = models.CharField(max_length=2, choices=EstadoEnvio.choices, verbose_name='Estado Anterior')
    estado_nuevo = models.CharField(max_length=2, choices=EstadoEnvio.choices, verbose_name='Estado Nuevo')
    observacion = models.TextField(blank=True, null=True, verbose_name='Observación')
    empleado = models.ForeignKey('envios.Empleado', on_delete=models.PROTECT, verbose_name='Empleado')
    fecha_cambio = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de Cambio')

    class Meta:
        verbose_name = 'Historial de Estado'
        verbose_name_plural = 'Historiales de Estado'
        ordering = ['-fecha_cambio']

    def __str__(self):
        return f"{self.encomienda.codigo}: {EstadoEnvio(self.estado_anterior).label} → {EstadoEnvio(self.estado_nuevo).label}"
