from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    # Supervisor connects per-bus: ws/bus/1/
    re_path(r'ws/bus/(?P<bus_id>\w+)/$', consumers.BusConsumer.as_asgi()),

    # Students connect to see all buses: ws/buses/
    re_path(r'ws/buses/$', consumers.AllBusesConsumer.as_asgi()),
]