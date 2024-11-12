"""
ASGI config for proyecto project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application

from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from channels.security.websocket import AllowedHostsOriginValidator

from sockets.router import websocket_urlpatterns

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'proyecto.settings')

application = ProtocolTypeRouter({
    'http': get_asgi_application(),
    'websocket' : AllowedHostsOriginValidator(
        AuthMiddlewareStack(
            URLRouter(
                websocket_urlpatterns,
                # Aquí se colocan las rutas de los consumers
            )
        )
    ),
})
