from django.shortcuts import render
from django.utils.safestring import mark_safe
import json
from django.contrib.auth.decorators import login_required

from .models import Chat
# Create your views here.

@login_required
def index(request):
    user = request.user
    
    chat_rooms = Chat.objects.filter(members = user)
    print(chat_rooms)
    context={
        
        
        
        'chat_rooms' : chat_rooms
    }
    
    
    
    return render(request, 'chat/index.html', context)


def room(request, room_name):
    username = request.user.email
    
    context = {

        'room_name': room_name,
        'username': mark_safe(json.dumps(username))
    }

    return render(request, 'chat/room.html', context)