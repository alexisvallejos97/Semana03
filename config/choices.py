from django.db import models

class EstadoGeneral(models.IntegerChoices):
    ACTIVO = 1, 'Activo'
    DE_BAJA = 9, 'De Baja'

class EstadoEnvio(models.TextChoices):
    PENDIENTE = 'PE', 'Pendiente'
    EN_TRANSITO = 'TR', 'En Tránsito'
    EN_DESTINO = 'DE', 'En Destino'
    ENTREGADO = 'EN', 'Entregado'
    DEVUELTO = 'DV', 'Devuelto'

class TipoDocumento(models.TextChoices):
    DNI = 'DNI', 'DNI'
    RUC = 'RUC', 'RUC'
    PASAPORTE = 'PAS', 'Pasaporte'
