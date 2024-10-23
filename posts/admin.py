from django.contrib import admin
from .models import Post , Media, Comment


class PostAdmin(admin.ModelAdmin):
    list_display = ('user',)


class MediaAdmin(admin.ModelAdmin):
    list_display = ('id', 'post')


class CommentAdmin(admin.ModelAdmin):
    list_display = ('user',)


admin.site.register(Post, PostAdmin)
admin.site.register(Media, MediaAdmin)
admin.site.register(Comment, CommentAdmin)
