import hashlib
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

# Create your models here.

class CustomerUser(AbstractUser):
    def __str__(self):
       return self.username

    def save(self, *args, **kwargs):
          self.set_password(self.password)
          super().save(*args, **kwargs)

def _createHash(value):
        string = value.encode('utf-8')
        print(string)
        return  hashlib.md5(string).hexdigest()

class OneOnOneChat(models.Model):
    initiator       = models.ForeignKey(CustomerUser, related_name='initiator', on_delete=models.CASCADE,null=True, blank=True )
    responder       = models.ForeignKey(CustomerUser, related_name='responder', on_delete=models.CASCADE,null=True, blank=True )
    hashtagid       = models.TextField(null=False, blank=False, unique=True, editable=False)
    addeddate       = models.DateTimeField('date added', editable=False, auto_now_add=True)
    removedate      = models.DateTimeField(null=True, blank=True)
    isDeleted       = models.BooleanField(default=False)
    
    def save(self, *args, **kwargs):
        #if self.hashtagid is None:
            hastag = f'{self.initiator.id}{self.initiator.username}{self.responder.id}{self.responder.username}'
            self.hashtagid = _createHash(hastag)
            super().save(*args, **kwargs)

class ChatGroup(models.Model):
    createdby       = models.ForeignKey(CustomerUser, related_name='group_createdby', on_delete=models.CASCADE,null=True, blank=True )
    deletedby       = models.ForeignKey(CustomerUser, related_name='group_deletedby', on_delete=models.CASCADE,null=True, blank=True )
    hashtagid       = models.TextField(null=False, blank=False, unique=True, editable=False)
    groupname       = models.CharField(null=False, blank=False, max_length=1024)
    removedate      = models.DateTimeField(null=True, blank=True)
    isDeleted       = models.BooleanField(default=False)
    addeddate       = models.DateTimeField('date published', editable=False, auto_now_add=True)

    def save(self, *args, **kwargs):
        #if self.hashtagid is None:
            hastag = f'{self.groupname}{self.createdby.id}{self.createdby.username}'
            self.hashtagid = _createHash(hastag)
            super().save(*args, **kwargs)

class UserMessages(models.Model):
    message         = models.TextField(null=False, blank=False)
    sender          = models.ForeignKey(CustomerUser, related_name='message_sender', on_delete=models.CASCADE,null=True, blank=True )
    receiver        = models.ForeignKey(CustomerUser, related_name='message_reciever', on_delete=models.CASCADE,null=True, blank=True )
    option          = models.CharField(max_length=16, default="chat")
    addeddate       = models.DateTimeField('date published', editable=False, auto_now_add=True)
    deletedby       = models.ForeignKey(CustomerUser, related_name='message_deletedby', on_delete=models.CASCADE,null=True, blank=True )
    removedate      = models.DateTimeField(null=True, blank=True)
    isDeleted       = models.BooleanField(default=False)

class GroupMembers(models.Model):
    groupmember    = models.ForeignKey(CustomerUser, related_name='group_member', on_delete=models.CASCADE,null=True, blank=True )
    chatgroup      = models.ForeignKey(ChatGroup, related_name='group', on_delete=models.CASCADE,null=True, blank=True )
    addeddate      = models.DateTimeField('date added', editable=False, auto_now_add=True)
    removedate     = models.DateTimeField(null=True, blank=True)
    isDeleted      = models.BooleanField(default=False)


'''class MessagesLog(models.Model):
    message         = models.CharField(max_length=2048)
    sender          = models.ForeignKey(CustomerUser, related_name='message_sender', on_delete=models.CASCADE,null=True, blank=True )
    receiver        = models.ForeignKey(CustomerUser, related_name='message_reciever', on_delete=models.CASCADE,null=True, blank=True )
    addeddate       = models.DateTimeField('date published', editable=False, auto_now_add=True)
    deletedby       = models.ForeignKey(CustomerUser, related_name='message_deletedby', on_delete=models.CASCADE,null=True, blank=True )
    removedate      = models.DateTimeField(null=True, blank=True)
    isDeleted       = models.BooleanField(default=False)'''
