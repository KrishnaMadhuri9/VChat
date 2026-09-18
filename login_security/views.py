from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.hashers import make_password,check_password
from django.contrib import messages
from django.http import JsonResponse
from django.db.models import Q

import json

from .models import Register,Comment
from .forms import RegisterForm,LoginForm,ProfileForm

from feeds.models import ImageFeed
from messenger.models import Notification,FriendRequest

# Create your views here.
def register_view(request):
    if request.method=="POST":
        form=RegisterForm(request.POST)
        if form.is_valid():
            password=make_password(form.cleaned_data['password'])
            user=form.save(commit=True)
            user.password=password
            user.save()
            messages.success(request,'Registered Successfully')
            return redirect('login')
    else:
        form=RegisterForm()
    return render(request,'register.html',{'forms':form})

def login_view(request):
    if request.method=="POST":
        form=LoginForm(request.POST)
        if form.is_valid():
            username=form.cleaned_data['username']
            password=form.cleaned_data['password']

            try:
                user=Register.objects.get(username=username)
                if check_password(password,user.password):
                    request.session['id']=user.id
                    request.session['username']=user.username

                    messages.success(request,'Logged-in Successfully')
                    return redirect('dashboard')
                else:
                    messages.error(request,'Password is not valid')
                    return redirect('login')
            except Register.DoesNotExist:
                messages.error(request,'Invalid credentials')
                return redirect('login')
    else:
        form=LoginForm()
    return render(request,'login.html',{'forms':form})

def logout_view(request):
    request.session.flush()
    messages.success(request,'Logged-out Successfully')
    return redirect('login')

def dashboard_view(request):
    if 'id' not in request.session:
        return redirect('login')
    
    user_id=request.session['id']
    user=Register.objects.get(id=user_id)

    sent_friend_ids = FriendRequest.objects.filter(sender=user,status="ACCEPTED").values_list("receiver_id",flat=True)
    sent_friend_names = Register.objects.filter(id__in=sent_friend_ids).values_list("username",flat=True)
    friend_names = ['admin',user.username]+list(sent_friend_names)
    feeds = ImageFeed.objects.filter(user_id__in=friend_names).order_by("-id")

    notifications=Notification.objects.filter(receiver=user).order_by("-created_at")
    
    return render(request,'dashboard.html',{'user':user.username,'feeds':feeds,"notifications":notifications})

def home_view(request):
    return render(request,'home.html')

def like_feed(request,id):
    if request.method=="POST":
        feed=get_object_or_404(ImageFeed,id=id)

        data=json.loads(request.body)
        liked=data.get("liked")

        if liked:
            feed.likecount+=1
        else:
            if feed.likecount>0:
                feed.likecount-=1
        feed.save()
        return JsonResponse({"likecount":feed.likecount,
                             "liked":liked})

def get_comments(request,id):
    comments=Comment.objects.filter(feed_id=id).order_by("-created_at")
    current_user=request.session['id']
    data=[]

    for comment in comments:
        data.append({
            "id":comment.id,
            "user":comment.user.username,
            "comment":comment.comment,
            "is_owner":comment.user.id==current_user
        })
    return JsonResponse({
        "comments":data
    })

def comment_feed(request,id):
    print("comment id",id)
    if request.method=="POST":
        data=json.loads(request.body)
        text=data.get('comment')
        feed=ImageFeed.objects.get(id=id)
        user_id=request.session['id']
        user=Register.objects.get(id=user_id)

        comment=Comment.objects.create(feed=feed,user=user,comment=text)
        comment.save()

        feed.commentcount += 1
        feed.save()

        return JsonResponse({
            "success":True,
            "commentcount":feed.commentcount
        })

def delete_comment(request,id):
    if request.method !="POST":
        return JsonResponse({"success":False},status=405)
    comment=get_object_or_404(Comment,id=id)
    current_user=request.session["id"]
    if comment.user.id!=current_user:
        return JsonResponse({"success":False,"message":"Permission denied"},status=403)
    feed=comment.feed
    comment.delete()
    if feed.commentcount>0:
        feed.commentcount -= 1
        feed.save()
    return JsonResponse({"success":True,
                         "commentcount":feed.commentcount})

def share_feed(request,id):
    if request.method=="POST":
        original=get_object_or_404(ImageFeed,id=id)
        user=Register.objects.get(id=request.session["id"])

        # Prevent sharing your own shared post
        if original.original_feed:
            original = original.original_feed

        ImageFeed.objects.create(
            user_id=user.username,
            title=original.title,
            image=original.image,
            like=original.like,
            comment=original.comment,
            share=original.share,
            original_feed=original
        )
        original.sharecount +=1
        original.save()
        return JsonResponse({
            "sharecount":original.sharecount,
            "message":"Post shared successfully."
        })

def profile_view(request):
    if 'id' not in request.session:
            return redirect('login')
        
    user_id=request.session['id']
    user=Register.objects.get(id=user_id)
    if request.method=="POST":
        # user.name=request.POST.get('name')
        # user.email=request.POST.get('email')
        # user.dob=request.POST.get('dob')
        # user.gender=request.POST.get('gender')
        # user.save()
        form=ProfileForm(request.POST,instance=user)
        if form.is_valid():
            form.save()
    else:
        form=ProfileForm(instance=user)
    return render(request,'profile.html',{'user':user.username,"profile":user,"form":form})