import httpx
from django.utils import timezone

CARRIER_API_URL = "https://api.transportista.pe/api/v1"
LOG_API_URL = "https://logs.empresa.pe/api/log"

async def verificar_estado_transportista(codigo_encomienda):
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(f"{CARRIER_API_URL}/envios/{codigo_encomienda}", timeout=10.0)
            if response.status_code == 200:
                return response.json()
        except Exception:
            pass
    return None

async def verificar_lotes_encomiendas(codigos):
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(f"{CARRIER_API_URL}/envios/lote", json={"codigos": codigos}, timeout=15.0)
            if response.status_code == 200:
                return response.json()
        except Exception:
            pass
    return []

async def enviar_notificacion_email(destinatario, asunto, mensaje):
    async with httpx.AsyncClient() as client:
        try:
            await client.post(
                f"{CARRIER_API_URL}/notificaciones/email",
                json={"para": destinatario, "asunto": asunto, "cuerpo": mensaje},
                timeout=10.0
            )
        except Exception:
            pass

async def registrar_log_externo(accion, detalles):
    async with httpx.AsyncClient() as client:
        try:
            await client.post(
                LOG_API_URL,
                json={"accion": accion, "detalles": detalles, "timestamp": timezone.now().isoformat()},
                timeout=5.0
            )
        except Exception:
            pass
