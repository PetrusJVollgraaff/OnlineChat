from django.db import connection
from .models import *

def SearchUsers(search):    
    row = []
    with connection.cursor() as cursor:
        cursor.execute('''
            SELECT 
                P.id, 
                P.name AS 'projectname', 
                P.descript AS 'projectdescript', 
                strftime('%d/%m/%Y %H:%M', P.addeddate) AS addeddate,
                P.completeddate, 
                            P.DueDate, 
                            PP.name AS 'priorityname', 
                            PP.level, 
                            PT.name AS 'typename', 
                            PT.descript AS 'typedescript',
                            S.staffname  
                        FROM projectsmanager_projects P
                        LEFT JOIN projectsmanager_priority AS PP    ON PP.id=P.priority_id
                        LEFT JOIN projectsmanager_type AS PT        ON PT.id=P.type_id
                        LEFT JOIN Staff AS S                             ON S.projectid = P.id 
                        WHERE P.isDeleted = 0
        ''')
        row = dictfetchall(cursor)       
        cursor.close()     
        
    return row

def UserContact(userid):
    row = []
    with connection.cursor() as cursor:
        cursor.execute(
            "SELECT * FROM( "+
            "    SELECT "+
            "        OC.responder_id AS 'id', "+
            "        OC.hashtagid AS 'queryid', "+
            "        CU.username AS 'username' "+
            "    FROM chatsystem_oneononechat OC "+
            "    LEFT JOIN chatsystem_customeruser CU ON CU.id = OC.responder_id "+
            "    WHERE OC.initiator_id=%s AND OC.isDeleted=0 "+
            
            "    UNION "+
            
            "    SELECT "+
            "        OC.initiator_id AS 'id', "+
            "        OC.hashtagid AS 'queryid', "+
            "        CU.username AS 'username' "+
            "    FROM chatsystem_oneononechat OC "+
            "    LEFT JOIN chatsystem_customeruser CU ON CU.id = OC.initiator_id "+
            "    WHERE OC.responder_id=%s AND OC.isDeleted=0 "+
            ") ORDER BY username "
        , [str(userid), str(userid)] )
        row = dictfetchall(cursor)       
        cursor.close()     
        
    return row

def UserGroup(userid):    
    row = []
    with connection.cursor() as cursor:
        cursor.execute(
            "SELECT "+
            "    CG.contact_id as id, "+
            "    CG.hashtagid as queryid, "+
            "    GM.groupname as groupname "+
                       
            "FROM chatsystem_groupmember GM "+
            "LEFT JOIN chatsystem_chatgroup CG ON CU.id = UCB.contact_id "+
            "WHERE CG.groupmember_id=%s AND CG.isDeleted=0 "
        ,[str(userid), str(userid)])
        row = dictfetchall(cursor)       
        cursor.close()     
        
    return row

def GetSingleChatM(userid, hashtag):
    row = []
    with connection.cursor() as cursor:        
        cursor.execute(
            "SELECT message, username FROM( "+
            "    SELECT "+
            "        UM.message AS 'message', "+
            "        CU.username AS 'username', "+
            "        UM.addeddate "+
            "    FROM chatsystem_usermessages UM "+
            "    JOIN chatsystem_oneononechat OC ON OC.initiator_id = UM.sender_id "+
            "    LEFT JOIN chatsystem_customeruser CU ON CU.id = OC.responder_id "+
            "    WHERE (UM.sender_id=%s OR UM.receiver_id=%s) "+
            "        AND UM.isDeleted=0 "+
            "        AND OC.hashtagid=%s "+
              
            "    UNION "+

            "    SELECT "+
            "        UM.message AS 'message', "+
            "        CU.username AS 'username', "+
            "        UM.addeddate "+
            "    FROM chatsystem_usermessages UM "+
            "    JOIN chatsystem_oneononechat OC ON OC.responder_id=UM.receiver_id "+
            "    LEFT JOIN chatsystem_customeruser CU ON CU.id = OC.initiator_id "+
            "    WHERE (UM.sender_id=%s OR UM.receiver_id=%s) "+
            "        AND UM.isDeleted=0 "+
            "        AND OC.hashtagid=%s "+
            ") ORDER BY addeddate "
        ,[str(userid), str(userid), hashtag, str(userid), str(userid), hashtag])
        row = dictfetchall(cursor)       
        cursor.close()     
        
    return row

def GetGroupChatM(userid, hashtag):
    row = []
    
    with connection.cursor() as cursor:        
        cursor.execute(
            "SELECT message, username FROM( "+
            "    SELECT "+
            "        UM.message AS 'message', "+
            "        CU.username AS 'username', "+
            "        UM.addeddate "+
            "    FROM chatsystem_usermessages UM "+
            "    JOIN chatsystem_oneononechat OC ON OC.initiator_id = UM.sender_id "+
            "    LEFT JOIN chatsystem_customeruser CU ON CU.id = OC.responder_id "+
            "    WHERE (UM.sender_id=%s OR UM.receiver_id=%s) "+
            "        AND UM.isDeleted=0 "+
            "        AND OC.hashtagid=%s "+
              
            "    UNION "+

            "    SELECT "+
            "        UM.message AS 'message', "+
            "        CU.username AS 'username', "+
            "        UM.addeddate "+
            "    FROM chatsystem_usermessages UM "+
            "    JOIN chatsystem_oneononechat OC ON OC.responder_id=UM.receiver_id "+
            "    LEFT JOIN chatsystem_customeruser CU ON CU.id = OC.initiator_id "+
            "    WHERE (UM.sender_id=%s OR UM.receiver_id=%s) "+
            "        AND UM.isDeleted=0 "+
            "        AND OC.hashtagid=%s "+
            ") ORDER BY addeddate "
        ,[str(userid), str(userid), hashtag, str(userid), str(userid), hashtag])
        row = dictfetchall(cursor)       
        cursor.close()     
        
    return row


def dictfetchall(cursor):
    "Return all rows from a cursor as a dict"
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]
