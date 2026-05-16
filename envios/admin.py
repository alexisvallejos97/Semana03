from django.contrib import admin
from .models import Empleado, Encomienda, HistorialEstado
from config.choices import EstadoEnvio

@admin.register(Empleado)
class EmpleadoAdmin(admin.ModelAdmin):
    list_display = ('codigo', 'nombres', 'apellidos', 'cargo', 'email', 'estado')
    list_filter = ('estado', 'cargo')
    search_fields = ('codigo', 'nombres', 'apellidos', 'email')

@admin.register(Encomienda)
class EncomiendaAdmin(admin.ModelAdmin):
    list_display = ('codigo', 'remitente', 'destinatario', 'ruta', 'estado_badge', 'fecha_registro')
    list_filter = ('estado', 'ruta')
    search_fields = ('codigo', 'remitente__nro_doc', 'destinatario__nro_doc')
    fieldsets = (
        ('Información General', {'fields': ('codigo', 'descripcion', 'peso_kg', 'volumen_cm3')}),
        ('Partes', {'fields': ('remitente', 'destinatario', 'ruta', 'empleado_registro')}),
        ('Estado y Costos', {'fields': ('estado', 'costo_envio', 'fecha_entrega_est', 'fecha_entrega_real', 'observaciones')}),
    )

    def estado_badge(self, obj):
        colors = {
            EstadoEnvio.PENDIENTE: 'orange',
            EstadoEnvio.EN_TRANSITO: 'blue',
            EstadoEnvio.EN_DESTINO: 'purple',
            EstadoEnvio.ENTREGADO: 'green',
            EstadoEnvio.DEVUELTO: 'red',
        }
        color = colors.get(obj.estado, 'gray')
        return f'<span style="color: {color}; font-weight: bold;">{obj.get_estado_display()}</span>'
    estado_badge.short_description = 'Estado'
    estado_badge.allow_tags = True

@admin.register(HistorialEstado)
class HistorialEstadoAdmin(admin.ModelAdmin):
    list_display = ('encomienda', 'estado_anterior', 'estado_nuevo', 'empleado', 'fecha_cambio')
    list_filter = ('estado_anterior', 'estado_nuevo')
