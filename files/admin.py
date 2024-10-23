from django.contrib import admin
from .models import File, Folder, Version


class FileAdmin(admin.ModelAdmin):
    list_display = ('user',)


class VersionAdmin(admin.ModelAdmin):
    list_display = ('id', 'file',)


class FolderAdmin(admin.ModelAdmin):
    list_display = ('user',)


admin.site.register(File, FileAdmin)
admin.site.register(Version, VersionAdmin)
admin.site.register(Folder, FolderAdmin)
