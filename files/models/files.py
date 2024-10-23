from django.db import models

class File(models.Model):
    user = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='files')
    name = models.CharField(max_length=255)
    public_id = models.CharField(max_length=255)
    url = models.URLField()
    type_file = models.CharField(max_length=10, choices=[
        ('imagen', 'Imagen'), ('video', 'Video')])
    folder = models.ForeignKey(
        'files.Folder', on_delete=models.CASCADE, related_name='files', null=True, blank=True)
    json_field = models.JSONField(blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Version(models.Model):
    file = models.ForeignKey(
        'files.File', on_delete=models.CASCADE, related_name='versions')
    url = models.URLField()
    description = models.TextField(max_length=500)
    public_id = models.CharField(max_length=255)
    json_field = models.JSONField(blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.file.name
