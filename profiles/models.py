from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver 
from sorl.thumbnail import ImageField 

class Profile(models.Model):
    user = models.OneToOneField(
        User, 
        on_delete=models.CASCADE,
        related_name="profile"
    )
    image = ImageField(upload_to="profiles")
    quote = models.CharField(max_length=255)
    blogger = models.BooleanField(default=False, blank=False)

    def __str__(self):
        return self.user.username
    
@receiver(post_save, sender=User)   # listens for the creation of objects of User type
def create_user_profile(sender, instance, created, **kwargs):
    """Create a new Profile() object when a Django User is created"""
    if created:
        Profile.objects.create(user=instance)


# Create your models here.
