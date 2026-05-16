from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import TemplateView, ListView, CreateView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.http import JsonResponse
from django.utils import timezone
from django.db.models import Count, Q
from .models import Encomienda, Empleado
from .forms import EncomiendaForm
from .serializers import serialize_encomienda
from config.choices import EstadoEnvio
import json

def get_empleado_from_user(user):
    if user.is_superuser:
        return Empleado.objects.filter(estado=1).first()
    return Empleado.objects.filter(email=user.email).first()

class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'envios/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        hoy = timezone.now().date()
        context['activas'] = Encomienda.objects.activas().count()
        context['en_transito'] = Encomienda.objects.en_transito().count()
        context['con_retraso'] = Encomienda.objects.con_retraso().count()
        context['entregadas_hoy'] = Encomienda.objects.filter(estado=EstadoEnvio.ENTREGADO, fecha_entrega_real=hoy).count()
        context['ultimas_actividades'] = Encomienda.objects.filter(
            estado__in=[EstadoEnvio.EN_TRANSITO, EstadoEnvio.ENTREGADO]
        ).order_by('-fecha_registro')[:10]
        return context

class EncomiendaListView(LoginRequiredMixin, ListView):
    model = Encomienda
    template_name = 'envios/encomienda_list.html'
    context_object_name = 'encomiendas'
    paginate_by = 15

    def get_queryset(self):
        qs = Encomienda.objects.con_relaciones().order_by('-fecha_registro')
        filtro = self.request.GET.get('filtro', 'todas')
        if filtro == 'pendientes':
            qs = qs.pendientes()
        elif filtro == 'transito':
            qs = qs.en_transito()
        elif filtro == 'entregadas':
            qs = qs.entregadas()
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filtro_actual'] = self.request.GET.get('filtro', 'todas')
        return context

class EncomiendaCreateView(LoginRequiredMixin, CreateView):
    model = Encomienda
    form_class = EncomiendaForm
    template_name = 'envios/encomienda_form.html'
    success_url = reverse_lazy('envios:encomienda_list')

    def form_valid(self, form):
        form.instance.empleado_registro = get_empleado_from_user(self.request.user)
        ruta = form.cleaned_data['ruta']
        encomienda = Encomienda.crear_con_costo_calculado(**form.cleaned_data)
        self.object = encomienda
        return redirect(self.success_url)

class EncomiendaDetailView(LoginRequiredMixin, DetailView):
    model = Encomienda
    template_name = 'envios/encomienda_detail.html'
    context_object_name = 'encomienda'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['estados_disponibles'] = EstadoEnvio.choices
        return context

def actualizar_estado_encomienda(request, pk):
    if request.method == 'POST':
        encomienda = get_object_or_404(Encomienda, pk=pk)
        nuevo_estado = request.POST.get('estado')
        observacion = request.POST.get('observacion', '')
        empleado = get_empleado_from_user(request.user)
        if empleado and nuevo_estado in dict(EstadoEnvio.choices):
            encomienda.cambiar_estado(nuevo_estado, empleado, observacion)
            return JsonResponse({'success': True, 'estado': nuevo_estado})
        return JsonResponse({'success': False, 'error': 'Datos inválidos'}, status=400)
    return JsonResponse({'success': False, 'error': 'Método no permitido'}, status=405)

def health_check(request):
    status = {'status': 'ok', 'database': 'unknown', 'redis': 'unknown', 'channels': 'unknown'}
    try:
        from django.db import connection
        connection.ensure_connection()
        status['database'] = 'connected'
    except Exception as e:
        status['database'] = f'error: {str(e)}'
        status['status'] = 'degraded'
    return JsonResponse(status)
