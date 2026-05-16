from django import forms
from .models import Encomienda
from config.choices import EstadoEnvio

class EncomiendaForm(forms.ModelForm):
    class Meta:
        model = Encomienda
        fields = ['descripcion', 'peso_kg', 'volumen_cm3', 'remitente', 'destinatario', 'ruta', 'observaciones']
        widgets = {
            'descripcion': forms.Textarea(attrs={'rows': 3, 'class': 'form-input', 'placeholder': 'Descripción del paquete'}),
            'peso_kg': forms.NumberInput(attrs={'class': 'form-input', 'step': '0.01', 'min': '0.01'}),
            'volumen_cm3': forms.NumberInput(attrs={'class': 'form-input', 'step': '0.01'}),
            'remitente': forms.Select(attrs={'class': 'form-select'}),
            'destinatario': forms.Select(attrs={'class': 'form-select'}),
            'ruta': forms.Select(attrs={'class': 'form-select'}),
            'observaciones': forms.Textarea(attrs={'rows': 2, 'class': 'form-input', 'placeholder': 'Observaciones adicionales (opcional)'}),
        }
        labels = {
            'descripcion': 'Descripción',
            'peso_kg': 'Peso (kg)',
            'volumen_cm3': 'Volumen (cm³)',
            'remitente': 'Remitente',
            'destinatario': 'Destinatario',
            'ruta': 'Ruta',
            'observaciones': 'Observaciones',
        }
