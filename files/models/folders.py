from django.db import models

class Folder(models.Model):
    user = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='folders')
    name = models.CharField(max_length=255)
    parent_folder = models.ForeignKey(
        'self', null=True, blank=True, on_delete=models.CASCADE, related_name='subcarpetas')
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
