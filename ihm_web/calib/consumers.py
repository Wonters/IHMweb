import json

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer

from .models import ProgressCalib


class CalibConsumer(WebsocketConsumer):

    def connect(self):
        self.name = 'calib'
        self.group_name = 'calibprogress'
        async_to_sync(self.channel_layer.group_add)(self.group_name, self.channel_name)
        self.accept()

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.group_name,
            self.channel_name,
        )
        pass

    def receive(self, text_data):
        data = {'current': ProgressCalib.current, 'total': ProgressCalib.total,
                'message': ProgressCalib.message}
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
