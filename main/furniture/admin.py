from django.contrib import admin

from .models import *


class FurnitureAdmin(admin.ModelAdmin):
    list_display = ('id','title','time_create','photo', 'is_published')
    list_display_links=('id','title')
    search_fields =('title', 'content')
    prepopulated_fields = {"slug": ("title",)}

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id','name')
    list_display_links = ('id','name')
    search_fields = ('name',)
    prepopulated_fields = {"slug":("name",)}


admin.site.register(Furniture, FurnitureAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Admincreatevote)
admin.site.register(ExpertVoted)
admin.site.register(ProductVote)
