from django.contrib import admin
from .models import *
from .forms import *


# Register your models here.
class PostAdmin(admin.ModelAdmin):
    form = PostForm
    list_display = ('title', 'author', 'content', 'location', 'image', 'created_at', 'updated_at')
    search_fields = ('title', 'location')
    readonly_fields = ('created_at', 'updated_at')

    fieldsets = (
        (None, {
            'fields': ('title', 'content', 'location', 'image', 'author')
        }),
    )


class CommentAdmin(admin.ModelAdmin):
    form = CommentForm


admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Location)
admin.site.register(Like)
