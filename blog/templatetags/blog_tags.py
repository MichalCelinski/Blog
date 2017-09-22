from django import template
from ..models import Article
from django.db.models import Count


register = template.Library()


@register.simple_tag
def total_articles():
    return Article.objects.count()


@register.inclusion_tag('blog/articles/latest_articles.html')
def show_latest_articles(count=3):
    latest_articles = Article.objects.order_by('-publish_date')[:count]
    return {'latest_articles': latest_articles}


@register.assignment_tag
def get_most_commented_articles(count=3):
    return Article.objects.annotate(total_comments=Count('comments')).order_by('-total_comments')[:count]
