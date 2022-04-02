import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from rest_framework.renderers import JSONRenderer
from .serializers import MessageSerializer

from .models import Room, Payam, DualPayam
from accounts.models import User

class ChatConsumer(WebsocketConsumer):
    def new_message(self, data):
        message = data['message']
        author = data['username']
        print(50*'1')
        print(data['roomname'])
        roomname =data['roomname']
        self.notif(data)
        user_model = User.objects.filter(email=author).last()

        chat_model = Room.objects.filter(roomname=roomname).first()
        if  chat_model :
            print(50*'5')
            print(chat_model)
            message_model = Payam.objects.create(user=user_model , content=message,related_chat=chat_model)
            result = eval(self.message_serializer(message_model))
            self.send_to_chat_message(result)          
        else :
            chat_model=Room.objects.create(roomname=roomname)
            chat_model.save(commit=False)
            chat_model.members.add(user_model)
            chat_model.save()

    def fetch_message(self, data):
        roomname = data['roomname']
        qs = Payam.last_message(self, roomname)

        print('fetch_message : '+roomname)
        print(25*'g')
        print(qs)
        message_json = self.message_serializer(qs)
        print(message_json)
        content = {
            
            "content" : eval(message_json),
            'command' : "fetch_message"
            
        }
        self.chat_message(content)

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
                    'content': data['message'],
                    '__str__' : data['username'],
                    'roomname' : message_roomname,
                    'members_list' : members_list
                
                }
            )    

    def image(self, data):
       self.send_to_chat_message(data)


    def message_serializer(self, qs):
    
        serialized = MessageSerializer(qs, many=(lambda qs : True if (qs.__class__.__name__ == 'QuerySet') else False)(qs))
        content = JSONRenderer().render(serialized.data)
        return content
    

    commands = {
        
        "new_message": new_message,
        "fetch_message": fetch_message,
        'img': image,
    
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
        print(50*'%')
        print(text_data_dict)
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
        print(50*'9')
        print(message) 
        content=  {
                'type': 'chat_message',
                'content': message['content'],
                'command':(lambda command : "img" if( command == "img") else "new_message")(command),
                '__str__' : message['__str__'],
             
            }
             
        async_to_sync(self.channel_layer.group_send)( self.room_group_name, content  )

    # Receive message from room group
    def chat_message(self, event):
        
        
        # Send message to WebSocket
        self.send(text_data=json.dumps(event))


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
        message_model=DualPayam.objects.create(content=content, roomname=roomname,sender=sender,reciever=reciever)
        result = eval(self.message_serializer(message_model))
        self.send_to_chat_message(result)


    commands = {
        
        
        'new_message': new_message
    
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
        print(50*'%')
        print(text_data_dict)
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
        print(50*'9')
        print(message) 
        content=  {
                'type': 'chat_message',
                'content': message['content'],
                'command':(lambda command : "img" if( command == "img") else "new_message")(command),
                '__str__' : message['__str__'],
             
            }
             
        async_to_sync(self.channel_layer.group_send)( self.room_group_name, content  )

    # Receive message from room group
    def chat_message(self, event):
        print(50*'w')
        print (event)

        # Send message to WebSocket
        self.send(text_data=json.dumps(event))


