import cloudinary
import cloudinary.api


def verify_cloudinary_credentials(cloud_name, api_key, api_secret):
    try:
        cloudinary.config(
            cloud_name=cloud_name,
            api_key=api_key,
            api_secret=api_secret,
        )
        cloudinary.api.ping()
        return True
    except Exception as e:
        return False


import calendar
import datetime
import uuid
from django.utils.text import slugify


def generate_slug():
    id = str(uuid.uuid4())
    return slugify('{}'.format(id[:13]))


def unique_slug_generator(instance):
    if instance.slug:
        return instance.slug
    else:
        slug = generate_slug()
        Klass = instance.__class__
        while (Klass.objects.filter(slug=slug).exists()):
            slug = generate_slug()
        return slug