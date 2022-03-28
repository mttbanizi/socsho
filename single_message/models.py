from django.db import models

from accounts.models import User

# Create your models here

class Room (models.Model):
    roomname = models.CharField(blank=True, max_length=50)
    user = models.ManyToManyField(User, null=True, blank=True,related_name="roomuser")
    
    
    def __str__(self):
        return self.roomname


class Payam(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="puser")
    content = models.TextField()
    related_chat = models.ForeignKey(Room, on_delete=models.CASCADE, blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    


    def last_message(self, roomname):
        return Message.objects.filter(related_chat__roomname=roomname)

    def __str__(self):
        return self.author.email

# Create your models here.
