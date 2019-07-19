from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from django.conf.urls import url
import carac.routing
#import calib.routing
from carac.consumers import ProgressConsumer
#from calib.consumers import CalibConsumer

application = ProtocolTypeRouter({
    'websocket': AuthMiddlewareStack(
        URLRouter([
            #url(r'^ws/calibprogress/$', CalibConsumer),
            url(r'^ws/progress/$', ProgressConsumer),
            ]
        ),
    ),
})
