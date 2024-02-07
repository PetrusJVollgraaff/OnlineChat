from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .models import *
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
def Chat(request, queryid, querytype):
    return render(request, "htmls/chatroom.html")


@csrf_exempt
@login_required(login_url='/')  
def GroupChat(request, queryid, querytype):
    return render(request, "htmls/chatroom.html")

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
            print("groupchat")
            messages = GetGroupChatM(userID, kwargs['queryid'])

    return JsonResponse(messages, safe=False )