from django.contrib import admin
from .models import Cliente

@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ('nro_doc', 'nombre_completo', 'tipo_doc', 'email', 'estado', 'fecha_registro')
    list_filter = ('estado', 'tipo_doc')
    search_fields = ('nro_doc', 'nombres', 'apellidos', 'email')
