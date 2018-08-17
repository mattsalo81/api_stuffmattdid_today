from django.contrib import admin
from .models import Post, Attachment, ImageAttachment, Tag

# Register your models here.
admin.site.register(Post)
admin.site.register(Attachment)
admin.site.register(ImageAttachment)
admin.site.register(Tag)
