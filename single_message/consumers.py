import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer

from .models import Room
from accounts.models import User

class ChatConsumer(WebsocketConsumer):
    def notif(self, data):

        message_roomname = data['roomname']
        chat_room_qs = Room.objects.filter(roomname=message_roomname)
        members_list = []
        i=0
        for room in chat_room_qs:
            for _ in chat_room_qs[i].user.all():
                
                members_list.append(_.email)
                i=i+1
        
        async_to_sync(self.channel_layer.group_send)(
            'chat_listener',
                {
                    'type': 'chat_message',
                    'message': data['message'],
                    '__str__' : data['username'],
                    'roomname' : message_roomname,
                    'members_list' : members_list
                
                }
            )    

    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
    
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        self.notif(text_data_json)
        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )

    # Receive message from room group
    def chat_message(self, event):
        message = event['message']

        # Send message to WebSocket
        self.send(text_data=json.dumps(event))