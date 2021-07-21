from django.contrib import admin
from .models import Post, Photo, Comment

class PostAdmin(admin.ModelAdmin):
    pass
admin.site.register(Post, PostAdmin)


class PhotoAdmin(admin.ModelAdmin):
    pass
admin.site.register(Photo, PhotoAdmin)


class CommentAdmin(admin.ModelAdmin):
    pass
admin.site.register(Comment, CommentAdmin)

# Register your models here.
