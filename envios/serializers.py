from config.choices import EstadoEnvio

def serialize_encomienda(encomienda):
    return {
        'id': encomienda.pk,
        'codigo': encomienda.codigo,
        'estado': encomienda.estado,
        'estado_display': EstadoEnvio(encomienda.estado).label,
        'descripcion': encomienda.descripcion_corta,
        'peso_kg': str(encomienda.peso_kg),
        'costo_envio': str(encomienda.costo_envio),
        'fecha_registro': encomienda.fecha_registro.isoformat(),
        'remitente': encomienda.remitente.nombre_completo,
        'destinatario': encomienda.destinatario.nombre_completo,
        'ruta': str(encomienda.ruta),
    }

def serialize_encomienda_detail(encomienda):
    data = serialize_encomienda(encomienda)
    data.update({
        'volumen_cm3': str(encomienda.volumen_cm3) if encomienda.volumen_cm3 else None,
        'fecha_entrega_est': encomienda.fecha_entrega_est.isoformat() if encomienda.fecha_entrega_est else None,
        'fecha_entrega_real': encomienda.fecha_entrega_real.isoformat() if encomienda.fecha_entrega_real else None,
        'observaciones': encomienda.observaciones,
        'dias_en_transito': encomienda.dias_en_transito,
        'tiene_retraso': encomienda.tiene_retraso,
        'historial': [
            {
                'estado_anterior': EstadoEnvio(h.estado_anterior).label,
                'estado_nuevo': EstadoEnvio(h.estado_nuevo).label,
                'observacion': h.observacion,
                'empleado': f"{h.empleado.nombres} {h.empleado.apellidos}",
                'fecha_cambio': h.fecha_cambio.isoformat(),
            }
            for h in encomienda.historial.all().order_by('-fecha_cambio')
        ]
    })
    return data
