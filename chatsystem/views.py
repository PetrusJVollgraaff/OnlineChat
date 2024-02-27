from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .models import *
from .function import *
from .userslog import *
from .SQL import *
import json
from urllib import parse
from django.urls import resolve


def index(request):
    if (request.user.is_authenticated):
        usercontacts    = UserContact(request.user.id) #UserContactsBook.objects.filter(owner=request.user.id, isDeleted=False)
        usergroups      = GroupMembers.objects.filter(groupmember=request.user.id, isDeleted=False)

        return render(request, "htmls/userlobby.html", {"contacts": usercontacts, "groups": usergroups})
    else:
        return render(request, "htmls/main.html")

@csrf_exempt
@login_required(login_url='/')  
def SearchUser(request):
    usercontacts = []
    
    if request.method == 'POST':
        jsonData    = json.loads(request.body)
        search      = jsonData.get("search")

        usercontacts    = CustomerUser.objects.filter(
            Q( username__icontains=search) 
            | Q(first_name__icontains=search) 
            | Q(last_name__icontains=search)
        )

        usercontacts = list(usercontacts.values("id", "username", "first_name", "last_name") )

    return JsonResponse(usercontacts, safe=False )

@csrf_exempt
@login_required(login_url='/')
def SearchOpen(request):
    if request.method == 'POST':
        user1 = request.user.id
        jsonData    = json.loads(request.body)
        user2      = jsonData.get("searchid")

        print(user1, user2)
        usercontacts = OneOnOneChat.objects.filter( 
            (Q( initiator_id=user1) & Q(responder_id=user2) ) 
            | (Q( initiator_id=user2) & Q(responder_id=user1) ) 
        )

        print(usercontacts, usercontacts[0].hashtagid)

        if(usercontacts == None):
            pass
        else:
            print("hello")
            return HttpResponseRedirect( f"/chat/{usercontacts[0].hashtagid}" )            



@csrf_exempt
@login_required(login_url='/')  
def MakeFirstContact(request):
    if request.method == 'POST':
        jsonData    = json.loads(request.body)
        search      = jsonData.get("search")

    pass

@csrf_exempt
@login_required(login_url='/')  
def AcceptContact(request):
    if request.method == 'POST':
        jsonData    = json.loads(request.body)
        search      = jsonData.get("search")


    
    pass



@csrf_exempt
@login_required(login_url='/')  
def Chat(request, queryid, querytype):
    #active_users = get_active_users()
    #print(active_users) 

    loginUser1 = request.user.id
    loginUser2 = GetUser2_ID(loginUser1, queryid)
    recieverSQL = CustomerUser.objects.get(id=loginUser2)
    isOnline = "offline"

    #if not active_users.get(id=loginUser2) == None:
    #    isOnline = "online"

    return render(request, "htmls/chatroom.html", 
                    {
                        "TopName": recieverSQL.username, 
                        "isOnline": isOnline, 
                        "queryid": queryid,
                        "querytype": querytype
                    }
                  )


@csrf_exempt
@login_required(login_url='/')  
def GroupChat(request, queryid, querytype):
    return render(request, "htmls/chatroom.html", {"TopName": "groupname"})

@csrf_exempt
@login_required(login_url='/')  
def getBubbles(request):
    messages    = []

    if request.method == 'GET':
        
        userID      = request.user.id
        parseurl    = parse.urlparse(request.META.get('HTTP_REFERER'))
    
        view, args, kwargs = resolve(parseurl[2])
        #print('test', kwargs, parseurl )

        if kwargs['querytype'] == "chat":
            messages = GetSingleChatM(userID, kwargs['queryid'])
        elif kwargs['querytype'] == "groupchat":
            #print("groupchat")
            messages = GetGroupChatM(userID, kwargs['queryid'])

    return JsonResponse(messages, safe=False )