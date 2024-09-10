from django.contrib import admin
from django.http import HttpRequest

from . import models
from .models import Article


# Register your models here.

class ArticleCategoryAdmin(admin.ModelAdmin):
    list_display = ['title', 'url_title', 'parent', 'is_active']
    list_editable = ['is_active', 'parent', 'url_title']


class ArticleAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug', 'author', 'is_active', 'published_date']
    list_editable = ['is_active']

    # when model is saving will be called
    def save_model(self, request: HttpRequest, obj: Article, form, change):
        if not change:
            obj.author = request.user
        return super().save_model(request, obj, form, change)


class ArticleCommentAdmin(admin.ModelAdmin):
    list_display = ['author', 'article', 'create_time', 'comment_text', 'parent']

    # when model is saving will be called
    def save_model(self, request: HttpRequest, obj: Article, form, change):
        if not change:
            obj.author = request.user
        return super().save_model(request, obj, form, change)


admin.site.register(models.Article, ArticleAdmin)
admin.site.register(models.ArticleCategory, ArticleCategoryAdmin)
admin.site.register(models.ArticleComment, ArticleCommentAdmin)
