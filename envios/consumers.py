import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.utils import timezone
from config.choices import EstadoEnvio

class EncomiendaConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        if self.scope["user"].is_anonymous:
            await self.close(code=4001)
        else:
            await self.channel_layer.group_add("encomiendas_global", self.channel_name)
            await self.accept()
            await self.send(text_data=json.dumps({"type": "connection", "status": "connected"}))

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard("encomiendas_global", self.channel_name)

    async def receive(self, text_data):
        data = json.loads(text_data)
        if data.get("action") == "ping":
            await self.send(text_data=json.dumps({"type": "pong", "timestamp": timezone.now().isoformat()}))
        elif data.get("action") == "subscribe":
            encomienda_id = data.get("encomienda_id")
            if encomienda_id:
                await self.channel_layer.group_add(f"encomienda_{encomienda_id}", self.channel_name)

    async def envio_actualizacion(self, event):
        await self.send(text_data=json.dumps(event))

class EncomiendaDetalleConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        if self.scope["user"].is_anonymous:
            await self.close(code=4001)
        else:
            self.encomienda_id = self.scope["url_route"]["kwargs"]["pk"]
            await self.channel_layer.group_add(f"encomienda_{self.encomienda_id}", self.channel_name)
            await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(f"encomienda_{self.encomienda_id}", self.channel_name)

    async def envio_actualizacion(self, event):
        await self.send(text_data=json.dumps(event))

class DashboardConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        if self.scope["user"].is_anonymous:
            await self.close(code=4001)
        else:
            await self.channel_layer.group_add("dashboard", self.channel_name)
            await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard("dashboard", self.channel_name)

    async def dashboard_actualizacion(self, event):
        await self.send(text_data=json.dumps(event))
