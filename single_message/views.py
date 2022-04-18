from optparse import Values
from django.dispatch import receiver
from django.shortcuts import render,redirect
from accounts.models import User
from .models import DualPayam
from itertools import chain, count 
from django.db.models import F , ExpressionWrapper, fields
from django.utils.timezone import utc
import datetime


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
    chat_list=chat_list_maker(request) 
    if sender :
        roomname= sender.roomname
        return render(request, "single_message/dual_room.html", {'reciever':user.email, 'roomname':roomname, 'chat_list':chat_list })
    else :
        roomname=str(user_id)+str(request.user.id)
        return render(request, "single_message/dual_room.html", {'reciever':user.email, 'roomname':roomname, 'chat_list':chat_list })

def dual_room_email(request,email):
    user= User.objects.get(email=email)
    # print(100*65)
    # print(str(user.id)+str(request.user.id))
    qs  =DualPayam.objects.filter(sender=user,reciever=request.user)
    chat_list=chat_list_maker(request) 
    for a in chat_list:
        print(a.timestamp)
    if qs :
        
        for message in qs :
            roomname= message.roomname
            if not message.is_read :
                message.is_read=True
                message.save()
        return render(request, "single_message/dual_room.html", {'reciever':user.email, 'roomname':roomname, 'chat_list':chat_list })
    else :
        roomname=str(user.id)+str(request.user.id)
        return render(request, "single_message/dual_room.html", {'reciever':user.email, 'roomname':roomname, 'chat_list':chat_list })    

   
def dual_room(request):
    chat_list=chat_list_maker(request) 
    print ("chat list")
    print (chat_list)

    for a in chat_list:
        roomname=a.roomname
        if a.reciever == request.user:
             reciever=a.sender.email
        else:
            reciever=a.reciever.email
        print(a.timestamp)
    # chat_list=DualPayam.objects.filter(Q(sender=request.user) | Q(reciever=request.user)).values()
    # print (chat_list)
    return render(request, "single_message/dual_room.html", {'reciever':reciever, 'chat_list':chat_list, 'roomname':roomname  })    

def chat_list_maker(request):
    now = datetime.datetime.utcnow().replace(tzinfo=utc)
    
    qs=DualPayam.objects.raw(
        'SELECT id, sender_id , reciever_id, MAX(timestamp), roomname FROM single_message_DualPayam WHERE sender_id = '+str(request.user.id)+' OR reciever_id = '+str(request.user.id)+' GROUP BY roomname ORDER BY timestamp DESC'
          )
    for a in qs:
        duration = now - a.timestamp
        
        if duration.days//365 > 0 :
            durations =str(duration.days//365) + ' years ago'
        elif duration.days//12 > 0 :
            durations =str(duration.days//12)+ ' months ago'
        elif duration.days > 0 :
            durations = str (duration.days)+' days ago'
        elif duration.seconds//3600 > 1 :
            durations = str(duration.seconds//3600) + ' hours ago'
        else :
            durations = str(duration.seconds//60)+' minutes ago'
        a.timestamp=durations
    
    return qs
