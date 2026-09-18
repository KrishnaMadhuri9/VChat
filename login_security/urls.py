from django.urls import path

from .views import register_view,login_view,logout_view,dashboard_view,home_view,like_feed,comment_feed,delete_comment,get_comments,share_feed,profile_view

urlpatterns=[
    path('',home_view,name='home'),
    path('login/',login_view,name='login'),
    path('register/',register_view,name='register'),
    path('dashboard/',dashboard_view,name='dashboard'),
    path('logout/',logout_view,name='logout'),
    path("like/<int:id>/",like_feed,name="like_feed"),
    path("comments/<int:id>/",get_comments,name="get_comments"),
    path("comment/<int:id>/",comment_feed,name="comment_feed"),
    path("delete-comment/<int:id>/",delete_comment,name='delete_comment'),
    path("share/<int:id>/",share_feed,name="share_feed"),
    path("profile/",profile_view,name="profile"),
]