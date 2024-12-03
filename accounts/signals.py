from django.dispatch import receiver
from django.db.models.signals import post_save

from accounts.models import CustomUser, UserProfile


@receiver(post_save, sender=CustomUser)
def save_post_create_profile_receiver(sender, instance, created, **kwargs):
    print(created)
    print(instance)
    if created:
        print("created")
        UserProfile.objects.create(user=instance)
    else:
        try:
            UserProfile.objects.get(user=instance).save()
        except:
            print("create user profile new ")
            UserProfile.objects.create(user=instance)
        print("Updated  user profile new ")
