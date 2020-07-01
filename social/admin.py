from django.contrib import admin

from .models import User,Post,Comment
# register both Post and Comment tables in the admin 
admin.site.register(Post)
admin.site.register(Comment)
