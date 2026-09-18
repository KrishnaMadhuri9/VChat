from django.db import models

# Create your models here.
class ImageFeed(models.Model):
    CHOICE_OPTIONS=(('YES','YES'),
                    ('NO','NO'))
    user_id=models.CharField(max_length=50)
    image=models.ImageField(upload_to='img/')
    title=models.CharField(max_length=500)
    like=models.CharField(max_length=20,choices=CHOICE_OPTIONS,default='NO')
    likecount=models.IntegerField(default=0)
    comment=models.CharField(max_length=20,choices=CHOICE_OPTIONS,default='NO')
    commentcount=models.IntegerField(default=0)
    share=models.CharField(max_length=20,choices=CHOICE_OPTIONS,default='NO')
    sharecount=models.IntegerField(default=0)
    original_feed=models.ForeignKey("self",on_delete=models.CASCADE, null=True,blank=True,related_name="shared_posts")

    def __str__(self):
        return self.user_id
    
class TextFeed(models.Model):
    user_id=models.CharField(max_length=50)
    text=models.TextField()
    background=models.CharField(max_length=100)
    like=models.BooleanField(default=False)
    comment=models.BooleanField(default=False)
    share=models.BooleanField(default=False)

    def __str__(self):
        return self.user_id
