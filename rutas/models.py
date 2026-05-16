from django.db import models
from config.choices import EstadoGeneral
from rutas.querysets import RutaQuerySet

class Ruta(models.Model):
    codigo = models.CharField(max_length=10, unique=True, verbose_name='Código')
    origen = models.CharField(max_length=100, verbose_name='Origen')
    destino = models.CharField(max_length=100, verbose_name='Destino')
    descripcion = models.TextField(blank=True, null=True, verbose_name='Descripción')
    precio_base = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Precio Base')
    dias_entrega = models.PositiveIntegerField(default=1, verbose_name='Días de Entrega')
    estado = models.IntegerField(choices=EstadoGeneral.choices, default=EstadoGeneral.ACTIVO, verbose_name='Estado')

    objects = RutaQuerySet.as_manager()

    class Meta:
        verbose_name = 'Ruta'
        verbose_name_plural = 'Rutas'
        ordering = ['origen', 'destino']

    def __str__(self):
        return f"{self.origen} → {self.destino} ({self.codigo})"
