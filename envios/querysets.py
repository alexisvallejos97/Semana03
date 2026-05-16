from django.db import models
from config.choices import EstadoEnvio

class EncomiendaQuerySet(models.QuerySet):
    def pendientes(self):
        return self.filter(estado=EstadoEnvio.PENDIENTE)

    def en_transito(self):
        return self.filter(estado=EstadoEnvio.EN_TRANSITO)

    def entregadas(self):
        return self.filter(estado=EstadoEnvio.ENTREGADO)

    def devueltas(self):
        return self.filter(estado=EstadoEnvio.DEVUELTO)

    def activas(self):
        return self.exclude(estado__in=[EstadoEnvio.ENTREGADO, EstadoEnvio.DEVUELTO])

    def por_ruta(self, ruta):
        return self.filter(ruta=ruta)

    def por_remitente(self, cliente):
        return self.filter(remitente=cliente)

    def por_destinatario(self, cliente):
        return self.filter(destinatario=cliente)

    def en_transito_por_ruta(self, ruta):
        return self.filter(estado=EstadoEnvio.EN_TRANSITO, ruta=ruta)

    def con_retraso(self):
        from django.utils import timezone
        return self.filter(
            fecha_entrega_est__lt=timezone.now().date(),
            estado__in=[EstadoEnvio.PENDIENTE, EstadoEnvio.EN_TRANSITO, EstadoEnvio.EN_DESTINO]
        )

    def con_relaciones(self):
        return self.select_related('remitente', 'destinatario', 'ruta', 'empleado_registro')
