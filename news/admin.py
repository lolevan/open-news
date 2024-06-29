# -*- coding: UTF-8 -*-
from django.contrib import admin
from django.utils.safestring import mark_safe
from django import forms

from ckeditor_uploader.widgets import CKEditorUploadingWidget

from .models import News, Category, Comment, Rating


class NewsAdminForm(forms.ModelForm):
    """
    ckeditor work form
    """
    content = forms.CharField(widget=CKEditorUploadingWidget())

    class Meta:
        """
        Form description
        """
        model = News
        fields = '__all__'


class NewsAdmin(admin.ModelAdmin):
    """
    This class is for the design of the admin panel
    """
    form = NewsAdminForm
    list_display = ('id', 'title', 'created_at', 'updated_at', 'is_published', 'get_photo')
    list_display_links = ('id', 'title')
    search_fields = ('title', 'content')
    list_editable = ('is_published',)
    list_filter = ('is_published', 'category')
    fields = (
        'title',
        'category',
        'content',
        'photo',
        'get_photo',
        'is_published',
        'views',
        'created_at',
        'updated_at',
    )
    readonly_fields = ('get_photo', 'views', 'created_at', 'updated_at',)
    save_on_top = True

    def get_photo(self, obj):
        """
        this function is return the miniature
        """
        if obj.photo:
            return mark_safe(f'<img src="{obj.photo.url}" width="75">')
        return '-'

    get_photo.short_description = 'Миниатюра'


class CategoryAdmin(admin.ModelAdmin):
    """
    This class is for the design of the admin panel
    """
    list_display = ('id', 'title')
    list_display_links = ('id', 'title')
    search_fields = ('title',)


class RatingAdmin(admin.ModelAdmin):
    """
    This class is for the design of the admin panel
    """
    list_display = ('id', 'user', 'news', 'value')
    list_display_links = ('id', 'user', 'news')
    search_fields = ('user', 'news')


admin.site.register(News, NewsAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Comment)
admin.site.register(Rating, RatingAdmin)

admin.site.site_title = 'Управление новостями'
admin.site.site_header = 'Управление новостями'
