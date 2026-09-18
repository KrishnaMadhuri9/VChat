from django.db import models

from feeds.models import ImageFeed

# Create your models here.
class Register(models.Model):
    CHOICE_OPTIONS=(("MALE","MALE"),
                    ("FEMALE","FEMALE"))
    username=models.CharField(max_length=100,unique=True)
    email=models.EmailField(max_length=254)
    dob=models.DateField()
    gender=models.CharField(max_length=20,choices=CHOICE_OPTIONS,default="MALE")
    password=models.CharField(max_length=254)

    def __str__(self):
        return self.username
    

class Comment(models.Model):
    feed=models.ForeignKey(ImageFeed, on_delete=models.CASCADE,related_name="feed_comments")
    user=models.ForeignKey(Register, on_delete=models.CASCADE)
    comment=models.TextField()
    created_at=models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}:{self.comment}"