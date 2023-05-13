from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import *

class WomenAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'time_create', 'get_html_photo', 'is_published')
    list_display_links = ('id', 'title')
    search_fields = ('title', 'content')
    list_editable = ('is_published',)
    list_filter = ('is_published', 'time_create')
    prepopulated_fields = {'slug':('title',)}
    fields = ('title', 'slug', 'cat', 'content', 'photo', 'get_html_photo', 'is_published', 'time_create', 'time_update')
    readonly_fields = ('time_create', 'time_update', 'get_html_photo')
    save_on_top = True

    def get_html_photo(self, object):
        if object.photo:
            return mark_safe(f'<img src="{object.photo.url}" width=50')

    get_html_photo.short_description = 'Миниатюра'

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')
    search_fields = ('name',) #если в кортеже один элемент, то нужно ставить ,
    prepopulated_fields = {'slug':('name',)}

class CommentAdmin(admin.ModelAdmin):
    list_display = ('name', 'post', 'text', 'time_create')
    list_display_links = ('name', )

class ContactAdmin(admin.ModelAdmin):
    list_display = ('email', 'name', 'is_check')
    list_display_links = ('email', )
    list_editable = ('is_check',)
    search_fields = ('name', )
    readonly_fields = ('email', )

admin.site.register(Women, WomenAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Contact, ContactAdmin)

admin.site.site_title = 'Админ-панель сайта о женщинах'
admin.site.site_header = 'Админ-панель сайта о женщинах'