from django.shortcuts import render

def index(request):
    return render(request, 'single_message/index.html', {})

def room(request, room_name):
    return render(request, 'single_message/room.html', {
        'room_name': room_name
    })