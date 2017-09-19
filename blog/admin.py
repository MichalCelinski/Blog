from django.contrib import admin
from .models import Article, Comment


class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'publish_date', 'article_status', 'slug')
    list_filter = ('article_status', 'create_date', 'publish_date', 'author')
    search_fields = ('title', 'body')
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'publish_date'
    ordering = ['article_status', 'publish_date']

admin.site.register(Article, ArticleAdmin)


class CommentAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'article', 'created', 'active')
    list_filter = ('created', 'active', 'updated')
    search_fields = ('name', 'email', 'comment')

admin.site.register(Comment, CommentAdmin)
