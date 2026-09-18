from django.shortcuts import render,redirect
from django.contrib import messages
from django.db.models import Q

from .models import ImageFeed,TextFeed
from login_security.models import Register

# Create your views here.
def FeedCreate_View(request):
    if 'id' not in request.session:
            return redirect('login')

    user_id=request.session['id']
    user=Register.objects.get(id=user_id)

    if request.method=="POST":
        user_id=user.username
        image=request.FILES.get('image')
        title=request.POST.get('title')
        like=request.POST.get('like')
        comment=request.POST.get('comment')
        share=request.POST.get('share')

        if not image is None:
            feed=ImageFeed.objects.create(user_id=user_id,image=image,title=title,like=like,comment=comment,share=share)
            feed.save()
            messages.success(request,'Post Uploaded successfully')
            return redirect('viewfeed')
        else:
            messages.error(request,'Reload Image')
            
    return render(request,'feedcreate.html',{"user":user.username})

def FeedView_View(request):
    if 'id' not in request.session:
        return redirect('login')

    user_id=request.session['id']
    user=Register.objects.get(id=user_id)

    feeds=ImageFeed.objects.filter(Q(user_id=user.username))#Q(user_id='admin')|
    return render(request,'feedview.html',{'feeds':feeds,'user':user.username})

def FeedUpdate_view(request,id):
    if 'id' not in request.session:
        return redirect('login')

    user_id=request.session['id']
    user=Register.objects.get(id=user_id)

    feed=ImageFeed.objects.get(id=id)

    if request.method=="POST":
        feed.user_id=user.username
        image=request.FILES.get('image')
        if image is not None:
            feed.image=image;
        feed.title=request.POST.get('title')
        
        feed.like=request.POST.get('like')
        feed.comment=request.POST.get('comment')
        feed.share=request.POST.get('share')

        if not feed.image is None:
            feed.save()
            messages.success(request,'Post Updated successfully')
            return redirect('viewfeed')
        else:
            messages.error(request,'Reload Image')

    return render(request,'feedupdate.html',{'feed':feed,'user':user.username})

def FeedDelete_view(request,id):
    if 'id' not in request.session:
        return redirect('login')

    user_id=request.session['id']
    user=Register.objects.get(id=user_id)

    feed=ImageFeed.objects.get(id=id)
    if request.method=="POST":
        feed.delete()
        return redirect('viewfeed')
    return render(request,'feeddelete.html',{'feed':feed,'user':user.username})