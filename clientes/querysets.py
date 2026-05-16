from django.db import models
from config.choices import EstadoGeneral

class ClienteQuerySet(models.QuerySet):
    def activos(self):
        return self.filter(estado=EstadoGeneral.ACTIVO)

    def de_baja(self):
        return self.filter(estado=EstadoGeneral.DE_BAJA)

    def con_dni(self):
        return self.filter(tipo_doc='DNI')

    def buscar(self, termino):
        from django.db.models import Q
        return self.filter(
            Q(nombres__icontains=termino) |
            Q(apellidos__icontains=termino) |
            Q(nro_doc__icontains=termino) |
            Q(email__icontains=termino)
        )
