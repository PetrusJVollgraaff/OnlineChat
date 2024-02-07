import json
from django.db.models import Q
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
from .models import UserMessages, OneOnOneChat, CustomerUser, GroupMembers, ChatGroup

class ChatSingle(WebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.gueryID = None
    
    def connect(self):
        self.gueryID = self.scope['url_route']['kwargs']['queryid']
        
        async_to_sync(self.channel_layer.group_add)(
            self.gueryID,
            self.channel_name
        )

        self.accept()

    def receive(self, text_data):
        senderID = self.scope['user'].id
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        isSend, username = oneonone_message( message, senderID, self.gueryID )

        if isSend:
            async_to_sync(self.channel_layer.group_send)(
                self.gueryID,{
                    'type':'chat_message',
                    'message':message,
                    'username': username,
                }
            )

    def chat_message(self, event):       
        message = event['message']
        username = event['username']

        self.send(text_data=json.dumps({
            'type':'chat',
            'message':message,
            'username': username,
        }))


class ChatGroups(WebsocketConsumer):
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.gueryID = None
    
    def connect(self):
        self.gueryID = self.scope['url_route']['kwargs']['queryid']

        async_to_sync(self.channel_layer.group_add)(
            self.gueryID,
            self.channel_name
        )

        self.accept()
   

    def receive(self, text_data):
        senderID = self.scope['user'].id
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        isSend, username = group_message(message, senderID, self.gueryID)

        if isSend:
            async_to_sync(self.channel_layer.group_send)(
                self.gueryID,
                {
                    'type':'chat_message',
                    'message':message,
                    'username': username,
                }
            )

    def chat_message(self, event):       
        message = event['message']
        username = event['username']

        self.send(text_data=json.dumps({
            'type':'chat',
            'message':message,
            'username': username,
        }))


def oneonone_message(message, sender, hastagid):
    isSend      = False
    reciever    = 0
    senderSQL   = CustomerUser.objects.get(id=sender)
    username    = senderSQL.username

    usercontacts    = OneOnOneChat.objects.filter( 
        (Q( initiator_id=sender) | Q(responder_id=sender) ) 
        & Q(hashtagid=hastagid)
    )
        
    if (not usercontacts == None):
        if (usercontacts[0].initiator_id == sender):
            reciever = usercontacts[0].responder_id
        elif(usercontacts[0].responder_id == sender):
            reciever = usercontacts[0].initiator_id

        if(reciever != 0):
            recieverSQL = CustomerUser.objects.get(id=reciever)

            messageSQL  = UserMessages(sender=senderSQL, message=message, receiver=recieverSQL, option="chat")
            messageSQL.save()
            isSend = True
        
    return isSend, username

def group_message(message, sender, hastagid):
    isSend      = False
    senderSQL   = CustomerUser.objects.get(id=sender)
    username    = senderSQL.username

    groupSQL    = ChatGroup.objects.filter( Q(hashtagid=hastagid) )
    isMember    = GroupMembers.objects.filter( Q(chatgroup_id=groupSQL.id) & Q(groupmember_id=sender))

        
    if (not isMember == None):
        messageSQL  = UserMessages(sender=senderSQL, message=message, receiver=groupSQL, option="groupchat")
        messageSQL.save()
        isSend = True
        
    return isSend, username