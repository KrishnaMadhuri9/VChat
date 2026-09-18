from django.urls import path
from .views import *

urlpatterns=[
    path('',FeedView_View,name='viewfeed'),
    path('add/',FeedCreate_View,name='addfeed'),
    path('update/<int:id>/',FeedUpdate_view,name='updatefeed'),
    path('delete/<int:id>/',FeedDelete_view,name='deletefeed'),
]
