from django.conf.urls import url
from channels.routing import ProtocolTypeRouter


from . import consumers

websocket_urlpatterns = [
    url(r'^ws/progress/$', consumers.ProgressConsumer),
]