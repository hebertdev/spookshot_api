from django.db import models

class Post(models.Model):
    user = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='posts')
    description = models.CharField(max_length=150)
    likes = models.ManyToManyField('users.User', related_name='likes', blank=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user} - {self.description[:20]}"  


class Media(models.Model):
    IMAGE = 'image'
    VIDEO = 'video'
    
    MEDIA_TYPE_CHOICES = [
        (IMAGE, 'Image'),
        (VIDEO, 'Video'),
    ]
    
    post = models.ForeignKey('posts.Post', on_delete=models.CASCADE, related_name='media')
    url = models.URLField()
    url_string = models.TextField()
    media_type = models.CharField(max_length=5, choices=MEDIA_TYPE_CHOICES)

    def __str__(self):
        return f"{self.media_type} - {self.url}"

class Comment(models.Model):
    user = models.ForeignKey('users.User', on_delete=models.CASCADE)
    post = models.ForeignKey('posts.Post', on_delete=models.CASCADE, related_name='comments')
    comment = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.user)






