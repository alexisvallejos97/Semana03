from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

def peso_positivo(value):
    if value <= 0:
        raise ValidationError(_('El peso debe ser mayor a 0.'))

def codigo_encomienda(value):
    if not value.startswith('ENC-'):
        raise ValidationError(_('El código debe comenzar con "ENC-".'))

def nro_doc_dni(value):
    if len(value) != 8 and not value.isdigit():
        raise ValidationError(_('El DNI debe tener 8 dígitos.'))
