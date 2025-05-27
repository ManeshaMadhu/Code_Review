from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class CodeReview(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    code_name = models.CharField(max_length=255)
    code = models.TextField(max_length=15000)
    error_response = models.TextField(max_length=15000, blank=True, null=True)
    enhance_response = models.TextField(max_length=15000, blank=True, null=True)
    optimize_response = models.TextField(max_length=15000, blank=True, null=True)

    def __str__(self):
        return f"{self.code_name} - {self.user.username}"

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=255, blank=True, null=True)  # You can add any field like role, etc.

    def __str__(self):
        return f"{self.user.username}'s Profile"
    

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)  # Creates the profile when a new user is created

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()  # Saves the profile whenever the user is saved