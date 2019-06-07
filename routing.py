from channels.routing import ProtocolTypeRouter
from .tests import ws_connect, ws_disconnect

application = ProtocolTypeRouter(
    {

    }
)

# channel_routing = [
#     route('websocket.connect', ws_connect),
#     route('websocket.disconnect', ws_disconnect),
# ]

