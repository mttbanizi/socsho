from django.shortcuts import render
from accounts.models import User
from .models import DualPayam
from itertools import chain 

def index(request):
    return render(request, 'single_message/index.html', {})

def room(request, room_name):
    return render(request, 'single_message/room.html', {
        'room_name': room_name
    })

def dual_room_id(request,user_id):
    user= User.objects.get(pk=user_id)
    print(100*65)
    print(str(user_id)+str(request.user.id))
    sender  =DualPayam.objects.filter(sender=user,reciever=request.user).last()
   
    if sender :
        roomname= sender.roomname
        return render(request, "single_message/dual_room.html", {'reciever':user.email, 'roomname':roomname })
    else :
        roomname=str(user_id)+str(request.user.id)
        return render(request, "single_message/dual_room.html", {'reciever':user.email, 'roomname':roomname })

def dual_room_email(request,email):
    user= User.objects.get(email=email)
    print(100*65)
    print(str(user.id)+str(request.user.id))
    qs  =DualPayam.objects.filter(sender=user,reciever=request.user)
     
   
    if qs :
        
        for message in qs :
            roomname= message.roomname
            if not message.is_read :
                message.is_read=True
                message.save()
        return render(request, "single_message/dual_room.html", {'reciever':user.email, 'roomname':roomname })
    else :
        roomname=str(user.id)+str(request.user.id)
        return render(request, "single_message/dual_room.html", {'reciever':user.email, 'roomname':roomname })    

   