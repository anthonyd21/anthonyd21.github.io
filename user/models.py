from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE,null=True,blank=True)
    email_confirmed = models.BooleanField(default=False)
    bio = models.CharField(max_length=150, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    avatar = models.ImageField(upload_to='media/%Y/%m/%d',default='static/user/defaultavatar.jpg')
    def __str__(self):
        return f"User {self.user.username}"

class Following(models.Model):
    user_id = models.ForeignKey("Profile", related_name="following", on_delete=models.CASCADE)
    following_user_id = models.ForeignKey("Profile", related_name="followers", on_delete=models.CASCADE)

class Post(models.Model):
    image = models.ImageField(upload_to='media/%Y/%m/%d',blank=False)
    text = models.CharField(max_length=2200)
    location = models.CharField(max_length=100)
    date = models.DateField(auto_now_add=True)
    owner = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="posts")
    likes = models.ManyToManyField(Profile, blank=True, related_name="likedposts")

    def __str__(self):
        return f"Post from {self.owner.user.first_name} at {self.location}"
    
@receiver(post_save, sender=User)
def update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()