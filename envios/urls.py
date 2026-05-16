from django.urls import path
from . import views
from . import views_async

app_name = 'envios'

urlpatterns = [
    path('dashboard/', views.DashboardView.as_view(), name='dashboard'),
    path('listado/', views.EncomiendaListView.as_view(), name='encomienda_list'),
    path('crear/', views.EncomiendaCreateView.as_view(), name='encomienda_create'),
    path('detalle/<int:pk>/', views.EncomiendaDetailView.as_view(), name='encomienda_detail'),
    path('encomienda/<int:pk>/actualizar/', views.actualizar_estado_encomienda, name='actualizar_estado'),
    path('health/', views.health_check, name='health_check'),
    path('api/dashboard-stats/', views_async.dashboard_stats_async, name='dashboard_stats_async'),
    path('api/encomienda/<int:pk>/cambiar-estado/', views_async.cambiar_estado_async, name='cambiar_estado_async'),
]
