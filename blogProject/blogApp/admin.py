from django.contrib import admin

# Register your models here.
from blogApp.models import Blog, Rating, Like, CustomUser, Category

admin.site.register(Blog)
admin.site.register(Rating)
admin.site.register(Category)
admin.site.register(CustomUser)
admin.site.register(Like)