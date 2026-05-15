from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
import json

class TestConsumer(WebsocketConsumer):
    def connect(self):
        # 1. Define your names first
        self.room_name = "test_consumer"
        # Match this EXACTLY with what is in models.py!
        self.room_group_name = "test_consumer_group" 

        # 2. Add this specific connection to the group layer
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name  
        )

        # 3. Accept the handshake connection last!
        self.accept()
        
        # Send a welcome message to confirm successful connection
        self.send(text_data=json.dumps({'status': 'connected'}))

    def receive(self, text_data):
        print(text_data)
        self.send(text_data=json.dumps(text_data))

    def disconnect(self, code):
        # Clean up by removing the channel from the group when they leave
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )
        print('disconnect')

    # This handles the broadcast from your model!
    def send_notification(self, event):
        print('send notification method triggered!')
        data = json.loads(event.get('value'))
        
        # 4. Don't forget to forward the message to the actual frontend client!
        self.send(text_data=json.dumps(data))