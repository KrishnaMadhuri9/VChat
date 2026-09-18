from django.shortcuts import render,redirect
from django.db.models import Q
from django.http import JsonResponse

from .models import FriendRequest,Notification,Message
from login_security.models import Register

# Create your views here.
def userlistview(request):
    if "id" not in request.session:
        return redirect('login')
    
    user_id=request.session['id']
    user=Register.objects.get(id=user_id)
    admin=Register.objects.get(username="admin")
    userlist = Register.objects.all().exclude(Q(id=user_id)|Q(id=admin.id))

    for other_user in userlist:
        friend_request=FriendRequest.objects.filter(sender=user,receiver=other_user).first()
        other_user.request_status=(friend_request.status if friend_request else "Follow")

    return render(request,'userlist.html',{"userlist":userlist,"user":user.username})

def sendrequest(request,receiveId):
    if "id" not in request.session:
        return JsonResponse({"status": "login_required"})

    if request.method != "POST":
        return JsonResponse({"status": "invalid_method"}, status=405)
    
    user_id=request.session['id']
    sender=Register.objects.get(id=user_id)
    receiver=Register.objects.get(id=receiveId)
    # friendrequest = FriendRequest.objects.filter(sender=sender,receiver=receiver).first()
    # if friendrequest:
    #     return JsonResponse({"status":friendrequest.status})
    
    friendrequest=FriendRequest.objects.create(sender=sender,receiver=receiver)
    friendrequest.save()
    Notification.objects.create(receiver=receiver,sender=sender,friend_request=friendrequest,message=f"{sender.username} sent you a friend request")
    return JsonResponse({"status":friendrequest.status})

def acceptrequest(request, notificationId):
    if "id" not in request.session:
        return JsonResponse({"status": "login_required"})

    if request.method != "POST":
        return JsonResponse({"status": "invalid_method"}, status=405) 
       
    user_id = request.session["id"]
    receiver = Register.objects.get(id=user_id)

    # Get notification belonging to logged-in user
    notification = Notification.objects.filter(id=notificationId,receiver=receiver).first()

    if not notification:
        return JsonResponse({"status": "not_found"})

    friendrequest = notification.friend_request

    # Only pending requests can be accepted
    if friendrequest.status == "PENDING":
        friendrequest.status = "ACCEPTED"
        friendrequest.save()

        notification.delete()
        return JsonResponse({"status": "ACCEPTED"})

    return JsonResponse({"status": friendrequest.status})

def rejectrequest(request, notificationId):
    if "id" not in request.session:
        return JsonResponse({"status": "login_required"})

    if request.method != "POST":
        return JsonResponse({"status": "invalid_method"}, status=405)

    user_id = request.session["id"]
    receiver = Register.objects.get(id=user_id)

    notification = Notification.objects.filter(id=notificationId,receiver=receiver).first()

    if not notification:
        return JsonResponse({"status": "not_found"})

    friendrequest = notification.friend_request
    # Only pending requests can be rejected
    if friendrequest.status == "PENDING":

        friendrequest.status = "REJECTED"
        friendrequest.save()

        notification.delete()
        return JsonResponse({"status": "REJECTED"})

    return JsonResponse({"status": friendrequest.status})


def friendslist(request):
    if "id" not in request.session:
        return redirect("login")

    user_id = request.session["id"]
    user = Register.objects.get(id=user_id)
    sent_friends = FriendRequest.objects.filter(sender=user,receiver__isnull=False,status="ACCEPTED").values_list("receiver",flat=True)
    received_friends = FriendRequest.objects.filter(receiver=user,sender__isnull=False,status="ACCEPTED").values_list("sender",flat=True)
    friend_ids = list(sent_friends) + list(received_friends)
    friends = Register.objects.filter(id__in=friend_ids)
    return render(request,"friends.html",{"friends": friends,"user": user.username})

def chatview(request, friendId):
    if "id" not in request.session:
        return redirect("login")

    user_id = request.session["id"]
    user = Register.objects.get(id=user_id)
    friend = Register.objects.get(id=friendId)

    # Check that they are actually accepted friends
    friendship_exists = FriendRequest.objects.filter(
        Q(sender=user,receiver=friend,status="ACCEPTED")
        |
        Q(sender=friend,receiver=user,status="ACCEPTED")).exists()

    if not friendship_exists:
        return redirect("friendslist")

    return render(request,"chat.html",{"user": user.username,"friend": friend})

def sendmessage(request, friendId):
    if "id" not in request.session:
        return JsonResponse({"status": "login_required"})

    if request.method != "POST":
        return JsonResponse({"status": "invalid_method"})

    user_id = request.session["id"]
    sender = Register.objects.get(id=user_id)
    receiver = Register.objects.get(id=friendId)

    # Check friendship
    friendship_exists = FriendRequest.objects.filter(
        Q(sender=sender,receiver=receiver,status="ACCEPTED")
        |
        Q(sender=receiver,receiver=sender,status="ACCEPTED")).exists()

    if not friendship_exists:
        return JsonResponse({"status": "not_friends"})

    message_text = request.POST.get("message")

    if not message_text:
        return JsonResponse({"status": "empty"})

    message = Message.objects.create(sender=sender,receiver=receiver,message=message_text)

    return JsonResponse({
        "status": "success",
        "id": message.id,
        "message": message.message,
        "sender": message.sender.username,
        "created_at": message.created_at.strftime(
            "%H:%M"
        )
    })

def getmessages(request, friendId):
    if "id" not in request.session:
        return JsonResponse({"status": "login_required"})

    user_id = request.session["id"]
    user = Register.objects.get(id=user_id)
    friend = Register.objects.get(id=friendId)

    # Check friendship
    friendship_exists = FriendRequest.objects.filter(
        Q(sender=user,receiver=friend,status="ACCEPTED")
        |
        Q(sender=friend,receiver=user,status="ACCEPTED")).exists()

    if not friendship_exists:
        return JsonResponse({"status": "not_friends"})

    messages = Message.objects.filter(
        Q(sender=user,receiver=friend)
        |
        Q(sender=friend,receiver=user)).order_by("created_at")

    message_list = []
    for msg in messages:
        message_list.append({
            "id": msg.id,
            "sender_id": msg.sender.id,
            "sender": msg.sender.username,
            "message": msg.message,
            "created_at": msg.created_at.strftime(
                "%H:%M"
            )
        })

    return JsonResponse({
        "status": "success",
        "messages": message_list
    })