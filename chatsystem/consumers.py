import json
from django.db.models import Q
from channels.generic.websocket import WebsocketConsumer, AsyncWebsocketConsumer
from asgiref.sync import async_to_sync
from .models import *
from .function import *

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

    def disconnect(self, close_code):
        # Remove the user from the WebSocket group
        self.channel_layer.group_discard(
            self.gueryID,
            self.channel_name
        )

    def receive(self, text_data):
        senderID = self.scope['user'].id
        data_json = json.loads(text_data)
        message = data_json['message']

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
    
    def disconnect(self, close_code):
        # Remove the user from the WebSocket group
        self.channel_layer.group_discard(
            self.gueryID,
            self.channel_name
        )

    def receive(self, text_data):
        senderID = self.scope['user'].id
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        

        isSend, username = group_message(message, senderID, self.gueryID)

        if isSend:
            '''async_to_sync(self.channel_layer.group_send)(
                self.gueryID,
                {
                    'type':'chat_message',
                    'message':message,
                    'username': username,
                }
            )'''

    def chat_message(self, event):       
        message = event['message']
        username = event['username']

        self.send(text_data=json.dumps({
            'type':'chat',
            'message':message,
            'username': username,
        }))


class VideoCallSingle(WebsocketConsumer):
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

    def disconnect(self, close_code):
        pass

    def receive(self, text_data):
        senderID = self.scope['user'].id
        data = json.loads(text_data)
        message_type = data['type']
        senderSQL   = CustomerUser.objects.get(id=senderID)
        name        = senderSQL.username
        print(data)
        
        if message_type == 'call':
            async_to_sync(self.channel_layer.group_send)(
                self.gueryID,
                {
                    'type': 'call_received',
                    'data': {
                        'caller': name,
                        'rtcMessage': data['rtcMessage']
                    }
                }
            )
        elif message_type == 'ignore':
            async_to_sync(self.channel_layer.group_send)(
                self.gueryID,
                {
                    'type': 'call_ignored',
                    'data': {
                        'caller': name
                    }
                }
            )
        elif message_type == 'call_end':
            async_to_sync(self.channel_layer.group_send)(
                self.gueryID,
                {
                    'type': 'call_ended',
                    'data': {
                        'caller': name
                    }
                }
            )

        '''if message_type == 'offer':
            # Handle SDP offer
            message = data['offer']
            # Save offer or forward it to the other peer
        elif message_type == 'answer':
            # Handle SDP answer
            message = data['answer']
            # Save answer or forward it to the other peer
        elif message_type == 'ice-candidate':
            # Handle ICE candidate
            message = data['candidate']
            # Save candidate or forward it to the other peer
        '''

        '''self.send(text_data=json.dumps({
            'type': new_type,
            'message': message
        }))'''

    def call_received(self, event):

        # print(event)
        #print('Call received by ', self.my_name )
        self.send(text_data=json.dumps({
            'type': 'call_received',
            'data': event['data']
        }))

    def call_ignored(self, event):
        # print(event)
        #print('Call received by ', self.my_name )
        self.send(text_data=json.dumps({
            'type': 'call_ignored',
            'data': event['data']
        }))
        
    def all_ended(self, event):
        # print(event)
        #print('Call received by ', self.my_name )
        self.send(text_data=json.dumps({
            'type': 'call_ended',
            'data': event['data']
        }))


class VideoCallGroup(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()

    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        await self.send(text_data=json.dumps({
            'message': message
        }))


class ScreenShare(AsyncWebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.gueryID = None
    
    async def connect(self):
        self.gueryID = self.scope['url_route']['kwargs']['queryid']
        
        async_to_sync(self.channel_layer.group_add)(
            self.gueryID,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
       pass

    async def receive(self, text_data):
        data = json.loads(text_data)
        message_type = data['type']
        print(data)

        if message_type == 'offer':
            # Handle SDP offer
            message = data['offer']
            # Save offer or forward it to the other peer
        elif message_type == 'answer':
            # Handle SDP answer
            message = data['answer']
            # Save answer or forward it to the other peer
        elif message_type == 'ice-candidate':
            # Handle ICE candidate
            message = data['candidate']
            # Save candidate or forward it to the other peer

        async_to_sync(self.channel_layer.group_send)(
                self.gueryID,{
                    'type': message_type,
                    message_type :data,
                }
            )

    async def send_message(self, message):
        await self.send(text_data=json.dumps(message))

    def save_offer(self, offer):
        # Customize this function to save the offer in your database
        # Example: You can create a model for rooms and store offers associated with a room
        pass

    def forward_offer(self, offer):
        # Customize this function to forward the offer to the other peer(s) in the same room
        # Example: You can use Django Channels to send the offer to the relevant consumers in the same room
        pass

    

def oneonone_message(message, sender, hastagid):
    isSend      = False
    reciever    = 0
    senderSQL   = CustomerUser.objects.get(id=sender)
    username    = senderSQL.username

    reciever = GetUser2_ID(sender, hastagid)
    '''usercontacts    = OneOnOneChat.objects.filter( 
        (Q( initiator_id=sender) | Q(responder_id=sender) ) 
        & Q(hashtagid=hastagid)
    )
        
    if (not usercontacts == None):
        if (usercontacts[0].initiator_id == sender):
            reciever = usercontacts[0].responder_id
        elif(usercontacts[0].responder_id == sender):
            reciever = usercontacts[0].initiator_id
'''
    if(reciever != 0):
        recieverSQL = CustomerUser.objects.get(id=reciever)

        messageSQL  = UserMessages(sender=senderSQL, message=message, receiver=recieverSQL, option="chat")
        messageSQL.save()
        isSend = True
        
    return isSend, username, 

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
