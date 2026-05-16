from django.db import models
from config.choices import EstadoGeneral, TipoDocumento
from clientes.querysets import ClienteQuerySet

class Cliente(models.Model):
    tipo_doc = models.CharField(max_length=10, choices=TipoDocumento.choices, verbose_name='Tipo de Documento')
    nro_doc = models.CharField(max_length=15, unique=True, verbose_name='Número de Documento')
    nombres = models.CharField(max_length=100, verbose_name='Nombres')
    apellidos = models.CharField(max_length=100, verbose_name='Apellidos')
    telefono = models.CharField(max_length=15, blank=True, null=True, verbose_name='Teléfono')
    email = models.EmailField(blank=True, null=True, verbose_name='Email')
    direccion = models.TextField(blank=True, null=True, verbose_name='Dirección')
    estado = models.IntegerField(choices=EstadoGeneral.choices, default=EstadoGeneral.ACTIVO, verbose_name='Estado')
    fecha_registro = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de Registro')

    objects = ClienteQuerySet.as_manager()

    class Meta:
        verbose_name = 'Cliente'
        verbose_name_plural = 'Clientes'
        ordering = ['-fecha_registro']

    def __str__(self):
        return f"{self.nombre_completo} ({self.nro_doc})"

    @property
    def nombre_completo(self):
        return f"{self.nombres} {self.apellidos}"

    @property
    def esta_activo(self):
        return self.estado == EstadoGeneral.ACTIVO

    @property
    def total_encomiendas_enviadas(self):
        return self.envios_como_remitente.count()
