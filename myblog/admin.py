from django.contrib import admin

# Register your models here.
from myblog.models import Post

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

admin.site.register(Post, PostAdmin)
