from django.urls import re_path

from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/dual_message/(?P<room_name>\w+)/$', consumers.DualChatConsumer.as_asgi()),
]