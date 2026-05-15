from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
import json

class TestConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name = "test_consumer"
        self.room_group_name = "test_consumer"

        self.accept()

        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name  # This is the unique pointer to this specific connection
        )
        self.send(text_data=json.dumps({'status': 'connected'}))

    def receive(self, text_data):
        print(text_data)
        self.send(text_data=json.dumps(text_data))

    def disconnect(self, code):
        print('disconnect')
