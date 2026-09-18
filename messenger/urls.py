from django.urls import path
from . import views

urlpatterns=[
    path('list/',views.userlistview,name='userlist'),
    path('sendrequest/<int:receiveId>/',views.sendrequest,name="sendrequest"),
    path("sendresponse/accept/<int:notificationId>/",views.acceptrequest,name="acceptrequest"),
    path("sendresponse/reject/<int:notificationId>/",views.rejectrequest,name="rejectrequest"),
    path("friends/",views.friendslist,name="friendslist"),
    path("chat/<int:friendId>/",views.chatview,name="chat"),
    path("chat/<int:friendId>/send/",views.sendmessage,name="sendmessage"),
    path("chat/<int:friendId>/messages/",views.getmessages,name="getmessages"),
]