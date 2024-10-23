from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save

class Profile(models.Model):
    user = models.OneToOneField('users.User', on_delete=models.CASCADE)
    avatar = models.ImageField(
        'profile picture',
        upload_to='users/pictures/',
        blank=True,
        null=True
    )
    bio = models.TextField('biography', blank=True, max_length=250)
    link = models.URLField('link', blank=True, max_length=250)

    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        """Return user's str representation."""
        return str(self.user)


@receiver(post_save, sender='users.User')
def ensure_profile_exists(sender, instance, **kwargs):
    if kwargs.get('created', False):
        Profile.objects.get_or_create(user=instance)
