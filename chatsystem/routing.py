from django.urls import re_path, path
from . import consumers

websocket_urlpatterns = [
    path('ws/chat/<str:queryid>/', consumers.ChatSingle.as_asgi(), name="wschat"),
    path('ws/video/<str:queryid>/', consumers.VideoCallSingle.as_asgi(), name="wsvideochat"),
    path('ws/groupchat/<str:queryid>/', consumers.ChatGroups.as_asgi(), name="wsgroupchat")
]