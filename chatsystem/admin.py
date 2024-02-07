from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomerUser, OneOnOneChat


# Register your models here.
admin.site.register(CustomerUser)
admin.site.register(OneOnOneChat)