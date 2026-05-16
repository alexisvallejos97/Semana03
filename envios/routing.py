from django.urls import path
from . import consumers

websocket_urlpatterns = [
    path('ws/encomiendas/', consumers.EncomiendaConsumer.as_asgi()),
    path('ws/encomiendas/<int:pk>/', consumers.EncomiendaDetalleConsumer.as_asgi()),
    path('ws/dashboard/', consumers.DashboardConsumer.as_asgi()),
]
