import json

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer

from .models import Progressbar, Campagnmodel


class ProgressConsumer(WebsocketConsumer):

    def connect(self):
        self.name = 'carac'
        self.group_name = 'progress'

        async_to_sync(self.channel_layer.group_add)(self.group_name, self.channel_name)
        self.accept()

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.group_name,
            self.channel_name,
        )
        pass

    def receive(self, text_data):
        data = {'current': Progressbar.current, 'total': Progressbar.total,
                'tc_current': Progressbar.tc_current, 'tc_total': Progressbar.tc_total,
                'tc': Progressbar.tc, 'temperature': Progressbar.temperature,
                'state': Progressbar.state, 'responseTask': Progressbar.responseTask, 'name': Campagnmodel.campagn_name,
                'type': Campagnmodel.campagn_type, 'date': Campagnmodel.campagn_date,
                'clim': Campagnmodel.campagn_climChamber, 'channels': Campagnmodel.campagn_channels,
                'clim_current': Campagnmodel.campagm_clim_current, 'clim_total': Campagnmodel.campagn_clim_total,
                'tc2play': Campagnmodel.campagn_tc2play, 'templist': Campagnmodel.campagn_templist}
        self.send_async_group(json.dumps(data))

    def progress_message(self, event):
        message = event['message']
        self.send(text_data=json.dumps({
            'message': message
        }))

    def send_async_group(self, message):
        async_to_sync(self.channel_layer.group_send)(
            self.group_name,
            {
                'type': 'progress_message',
                'message': message
            }
        )
