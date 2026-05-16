# Laudesciende - Sistema de Gestión de Encomiendas

Sistema web para la gestión de envíos y encomiendas con actualizaciones en tiempo real.

## Tecnologías

- **Backend:** Django 6.0.4 (Python 3.12)
- **Base de datos:** PostgreSQL 15
- **Tiempo real:** Django Channels + WebSockets
- **Broker:** Redis 7
- **Frontend:** Tailwind CSS + Vanilla JS
- **Contenedores:** Docker + Docker Compose

## Inicio Rápido

```bash
cd laudesciende
docker-compose up --build
```

Accede a:
- **Aplicación:** http://localhost:8000
- **pgAdmin:** http://localhost:5050

## Datos de Ejemplo

```bash
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py seed
```

### Usuarios de prueba

| Usuario | Contraseña | Rol |
|---------|------------|-----|
| admin | admin123 | Administrador |
| operador1 | operador123 | Operador |
| operador2 | operador123 | Operador |

## Funcionalidades

- Dashboard con estadísticas en tiempo real
- CRUD de encomiendas
- Seguimiento de estados (Pendiente, En Tránsito, En Destino, Entregado, Devuelto)
- Notificaciones WebSocket en vivo
- Cálculo automático de costos de envío
- Historial de cambios de estado
- Gestión de clientes, rutas y empleados

## Estructura

```
laudesciende/
├── config/          # Configuración Django
├── clientes/        # App de clientes
├── rutas/           # App de rutas
├── envios/          # App principal de encomiendas
├── templates/       # Templates HTML
├── static/          # Archivos estáticos
└── docker-compose.yml
```
