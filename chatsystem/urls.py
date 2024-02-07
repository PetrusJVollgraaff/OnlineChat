from django.urls import path
from . import views, login

urlpatterns = [
    path("login", login.login_view, name="login"),
    path("logout", login.logout_view, name="logout"),
    path("register", login.register, name="register"),
    
    path('', views.index, name='index'),
    path("getBubbles", views.getBubbles, name="getbubbles"),
    path("<str:querytype>/<str:queryid>/", views.Chat, name="chat"),
    path("<str:querytype>/<str:queryid>/", views.GroupChat, name="groupchat"),
    path("SearchUser", views.SearchUser, name='searchuser')
]