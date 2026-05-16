import pytest
import json
from channels.testing import WebsocketCommunicator
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from django.contrib.auth.models import User
from envios.consumers import EncomiendaConsumer, DashboardConsumer

@pytest.mark.asyncio
@pytest.mark.django_db
async def test_unauthenticated_rejection():
    communicator = WebsocketCommunicator(EncomiendaConsumer.as_asgi(), "/ws/encomiendas/")
    connected, _ = await communicator.connect()
    assert not connected
    await communicator.close()

@pytest.mark.asyncio
@pytest.mark.django_db
async def test_authenticated_connection():
    user = await User.objects.acreate(username='testuser', password='testpass')
    communicator = WebsocketCommunicator(EncomiendaConsumer.as_asgi(), "/ws/encomiendas/")
    communicator.scope["user"] = user
    connected, _ = await communicator.connect()
    assert connected
    await communicator.disconnect()

@pytest.mark.asyncio
@pytest.mark.django_db
async def test_ping_pong():
    user = await User.objects.acreate(username='testuser2', password='testpass')
    communicator = WebsocketCommunicator(EncomiendaConsumer.as_asgi(), "/ws/encomiendas/")
    communicator.scope["user"] = user
    connected, _ = await communicator.connect()
    assert connected
    await communicator.send_json_to({"action": "ping"})
    response = await communicator.receive_json_from()
    assert response["type"] == "pong"
    await communicator.disconnect()

@pytest.mark.asyncio
@pytest.mark.django_db
async def test_channel_layer_notification():
    channel_layer = get_channel_layer()
    await channel_layer.group_send("encomiendas_global", {"type": "envio.actualizacion", "test": "data"})

@pytest.mark.asyncio
@pytest.mark.django_db
async def test_dashboard_connection():
    user = await User.objects.acreate(username='dashuser', password='testpass')
    communicator = WebsocketCommunicator(DashboardConsumer.as_asgi(), "/ws/dashboard/")
    communicator.scope["user"] = user
    connected, _ = await communicator.connect()
    assert connected
    await communicator.disconnect()

@pytest.mark.asyncio
@pytest.mark.django_db
async def test_dashboard_stats_update():
    channel_layer = get_channel_layer()
    await channel_layer.group_send("dashboard", {"type": "dashboard.actualizacion", "accion": "test"})
