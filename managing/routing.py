from django.urls import re_path

from managing import consumers

websocket_urlpatterns = [
    re_path(r'ws/chat/(?P<room_name>\w+)/$', consumers.ChatConsumer),
    re_path(r'ws/bot/(?P<room_name>\w+)/$', consumers.BotConsumer),
]