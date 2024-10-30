from django.db import models
from django.db.models.signals import post_save, pre_save

#utisl
from utils import unique_slug_generator

class Cloudname(models.Model):
    slug = models.SlugField(unique=True, blank=True , null=True)
    user = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='cloudnames')
    cloudname = models.CharField('cloudname', max_length=150)
    public_key = models.CharField('public key', max_length=150)
    secret_key = models.CharField('secret key', max_length=150) 

    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return user.username + self.cloudname

def set_slug(sender, instance, *args, **kwargs):
    instance.slug = unique_slug_generator(instance)


pre_save.connect(set_slug, sender=Cloudname)
post_save.connect(set_slug, sender=Cloudname)
