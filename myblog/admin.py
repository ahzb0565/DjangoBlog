from django.contrib import admin

# Register your models here.
from myblog.models import Post, Comment

class PostAdmin(admin.ModelAdmin):
    """
    For Post to register to admin site. 
    It contains the list display/ many kinds of fields etc.
    """
    list_display = ("title", "slug", "author", "publish", "status")
    list_filter = ("status", "created", "publish", "author")
    search_fields = ("title", "body")
    prepopulated_fields = {'slug': ('title',)}
    raw_id_fields = ("author",)
    date_hierarchy = "publish"
    ordering = ["status", "publish"]

class CommentAdmin(admin.ModelAdmin):
    '''
    The comments admin class registered in admin site
    '''
    list_display = ('name', 'email', 'post', 'created', 'active')
    list_filter = ('active', 'created', 'updated')
    search_fields = ('name', 'email', 'body')


admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)
