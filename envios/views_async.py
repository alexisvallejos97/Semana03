import json
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from .models import Encomienda, Empleado
from config.choices import EstadoEnvio

async def dashboard_stats_async(request):
    activas = await Encomienda.objects.activas().acount()
    en_transito = await Encomienda.objects.en_transito().acount()
    con_retraso = await Encomienda.objects.con_retraso().acount()
    hoy = timezone.now().date()
    entregadas_hoy = await Encomienda.objects.filter(
        estado=EstadoEnvio.ENTREGADO, fecha_entrega_real=hoy
    ).acount()
    return JsonResponse({
        'activas': activas,
        'en_transito': en_transito,
        'con_retraso': con_retraso,
        'entregadas_hoy': entregadas_hoy,
    })

@login_required
async def cambiar_estado_async(request, pk):
    if request.method == 'POST':
        try:
            encomienda = await Encomienda.objects.aget(pk=pk)
            data = json.loads(request.body)
            nuevo_estado = data.get('estado')
            observacion = data.get('observacion', '')
            empleado = await Empleado.objects.filter(email=request.user.email).afirst()
            if not empleado and request.user.is_superuser:
                empleado = await Empleado.objects.filter(estado=1).afirst()
            if empleado and nuevo_estado in dict(EstadoEnvio.choices):
                estado_anterior = encomienda.estado
                encomienda.estado = nuevo_estado
                if nuevo_estado == EstadoEnvio.ENTREGADO:
                    encomienda.fecha_entrega_real = timezone.now().date()
                await encomienda.asave()
                from .models import HistorialEstado
                await HistorialEstado.objects.acreate(
                    encomienda=encomienda,
                    estado_anterior=estado_anterior,
                    estado_nuevo=nuevo_estado,
                    observacion=observacion,
                    empleado=empleado
                )
                channel_layer = get_channel_layer()
                await channel_layer.group_send('encomiendas_global', {
                    'type': 'envio.actualizacion',
                    'encomienda_id': encomienda.pk,
                    'codigo': encomienda.codigo,
                    'estado_anterior': EstadoEnvio(estado_anterior).label,
                    'estado_nuevo': EstadoEnvio(nuevo_estado).label,
                    'observacion': observacion,
                    'empleado': f"{empleado.nombres} {empleado.apellidos}",
                    'fecha': timezone.now().isoformat(),
                })
                return JsonResponse({'success': True})
            return JsonResponse({'success': False, 'error': 'Datos inválidos'}, status=400)
        except Encomienda.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Encomienda no encontrada'}, status=404)
    return JsonResponse({'success': False, 'error': 'Método no permitido'}, status=405)
