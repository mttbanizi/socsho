import json
from django.dispatch import receiver

from django.http import request
from django.shortcuts import redirect
from django.shortcuts import render
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from rest_framework.renderers import JSONRenderer
from .serializers import MessageSerializer
from django.utils.timezone import utc
import datetime
from .models import Room, Payam, DualPayam
from accounts.models import User

class DualChatConsumer(WebsocketConsumer):
    
    def message_serializer(self, qs):
    
        serialized = MessageSerializer(qs, many=(lambda qs : True if (qs.__class__.__name__ == 'QuerySet') else False)(qs))
        content = JSONRenderer().render(serialized.data)
        return content

    def new_message(self,data):
        content = data['message']
        roomname =data['roomname']
        sender=User.objects.filter(email=data['sender']).last()
        reciever=User.objects.filter(email=data['reciever']).last()
        self.receiver=data['reciever']
        print(data['reciever'])
        now = datetime.datetime.utcnow().replace(tzinfo=utc)
        
        message_model=DualPayam.objects.create(content=content, roomname=roomname,sender=sender,reciever=reciever)
        duration = now - message_model.timestamp
        if duration.days//365 > 0 :
            durations =str(duration.days//365) + ' years ago'
        elif duration.days//12 > 0 :
            durations =str(duration.days//12)+ ' months ago'
        elif duration.days > 0 :
            durations = str (duration.days)+' days ago'
        elif duration.seconds//3600 > 1 :
            durations = str(duration.seconds//3600) + ' hours ago'
        else :
            durations = 'now'
        data['duration']=durations
        print(duration)
        result = eval(self.message_serializer(message_model))
        self.notif_reciever(data)
        self.send_to_chat_message(result)

    def notif_reciever(self, data):
        message_roomname = data['roomname']
        print(20*'Nooo')   
        print(data)     
        async_to_sync(self.channel_layer.group_send)(
            'chat_listener',
                {
                    'type': 'chat_message',
                    'content': data['message'],
                    '__str__' : data['sender'],
                    'reciever' :data['reciever'],
                    'roomname': message_roomname,
                    'duration': data['duration']
                
                }
            )    

    def fetch_message(self, data):
        roomname = data['roomname']
        # print('fetch_message : '+roomname)
        qs = DualPayam.objects.filter(roomname= roomname)
        # print(25*'g')
        # print(qs)
        message_json = self.message_serializer(qs)
        # print(message_json)
        content = {            
            "content" : eval(message_json),
            'command' : "fetch_message"
                        
        }
        self.chat_message(content)

    def set_read(self,data):
        # print ('set_read')
        # print(data)
        # print (self.scope['user'])
        qs= DualPayam.objects.filter(roomname=data['roomname'], is_read= False )
        for message in qs :
            message.is_read= True
            message.save()
            print (message.content)
    
    def unread_messages(self,data):
        #  print ('unread_messages')
        #  print(data)
         receiver=User.objects.get(email=data['username'])
         qs= DualPayam.objects.filter(reciever=receiver, is_read=False)
         message_json = self.message_serializer(qs)
        #  print(message_json)
         content = {            
            "content" : eval(message_json),
            'command' : "unread_messages"            
        }
         self.chat_message(content)

   



    commands = {
        'fetch_message':fetch_message,
        'new_message': new_message,
        'unread_messages': unread_messages,
        'set_read': set_read
    }

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
        text_data_dict = json.loads(text_data)
        command = text_data_dict['command']        
        # print(50*'%')
        # print(text_data_dict)
        self.commands[command](self, text_data_dict)
        # message = text_data_dict['message']
        # self.notif(text_data_dict)
        # Send message to room group
        # async_to_sync(self.channel_layer.group_send)(
        #     self.room_group_name,
        #     {
        #         'type': 'chat_message',
        #         'message': message
        #     }
        # )

    def send_to_chat_message(self, message):
        command = message.get("command", None)
        # print(50*'9')
        # print(message) 
        content=  {
                'type': 'chat_message',
                'content': message['content'],
                'command':(lambda command : "img" if( command == "img") else "new_message")(command),
                '__str__' : message['__str__'],
                'room_name': self.room_name,
                'receiver': self.receiver
             
            }
             
        async_to_sync(self.channel_layer.group_send)( self.room_group_name, content  )

    # Receive message from room group
    def chat_message(self, event):
        text_data=json.dumps(event)
        # print(50*'wW'+' : ')
        # print(self.scope['user'])
        # print (event)
        #print ( self.scope ) 
        # Send message to WebSocket
        self.send(text_data)


