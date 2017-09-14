from django.shortcuts import render, get_object_or_404
from django.views import View
from .models import Article


class ArticlesListView(View):

    def get(self, request):
        articles_list = Article.objects.filter(article_status='published')
        context = {'articles': articles_list}
        return render(request, 'blog/articles/list.html', context)


class ArticleView(View):

    def get(self, request, slug):
        article = get_object_or_404(Article,
                                    slug=slug,
                                    article_status='published')
        context = {'article': article}
        return render(request, 'blog/articles/details.html', context)
