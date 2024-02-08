from django.db.models import Q
from .models import UserMessages, OneOnOneChat, CustomerUser, GroupMembers, ChatGroup

def GetUser2_ID(user1, hastagid):
    reciever = 0
    
    usercontacts = OneOnOneChat.objects.filter( 
        (Q( initiator_id=user1) | Q(responder_id=user1) ) 
        & Q(hashtagid=hastagid)
    )

    if (not usercontacts == None):
        if (usercontacts[0].initiator_id == user1):
            reciever = usercontacts[0].responder_id
        elif(usercontacts[0].responder_id == user1):
            reciever = usercontacts[0].initiator_id

    return reciever