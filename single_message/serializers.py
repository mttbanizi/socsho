from rest_framework import serializers
from .models import Payam

class MessageSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Payam
        fields= ['__str__', 'content', 'timestamp']
    