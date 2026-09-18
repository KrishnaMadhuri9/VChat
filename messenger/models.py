from django.db import models

from login_security.models import Register

# Create your models here.
class FriendRequest(models.Model):
    Status_List=[("PENDING","PENDING"),
                 ("ACCEPTED","ACCEPTED"),
                 ("REJECTED","REJECTED")]
    sender=models.ForeignKey(Register,on_delete=models.CASCADE,related_name="send_friend_request")
    receiver=models.ForeignKey(Register,on_delete=models.CASCADE,related_name="receive_friend_request")
    status=models.CharField(max_length=20,choices=Status_List,default="PENDING")
    created_at=models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.sender} -> {self.receiver} ({self.status})"

class Notification(models.Model):
    receiver = models.ForeignKey(Register,on_delete=models.CASCADE,related_name="notifications")
    sender = models.ForeignKey(Register,on_delete=models.CASCADE,related_name="sent_notifications")
    friend_request = models.ForeignKey(FriendRequest,on_delete=models.CASCADE,related_name="notification")
    message = models.CharField(max_length=255)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

class Message(models.Model):
    sender = models.ForeignKey(Register,on_delete=models.CASCADE,related_name="sent_messages")
    receiver = models.ForeignKey(Register,on_delete=models.CASCADE,related_name="received_messages")
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sender} -> {self.receiver}: {self.message}"
