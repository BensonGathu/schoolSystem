"""
ASGI config for schoolSystem project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/asgi/
"""

import os
import django
from channels.routing import ProtocolTypeRouter,URLRouter
from channels.auth import AuthMiddlewareStack,AuthMiddleware
from django.core.asgi import get_asgi_application
from channels.security.websocket import AllowedHostsOriginValidator

from notifications import consumers
#from notifications.consumers import 
from notifications.routing import websocket_urlpatterns
from django.urls import re_path,path
import notifications.routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'schoolSystem.settings')
django.setup()

application =ProtocolTypeRouter({"http": get_asgi_application(),
                                "websocket": AllowedHostsOriginValidator(AuthMiddlewareStack(
                                    URLRouter(
            websocket_urlpatterns
        ))
                                )})

