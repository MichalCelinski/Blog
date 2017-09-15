from django.shortcuts import render, get_object_or_404
from django.views import View
from .models import Article
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


class ArticlesListView(View):

    def get(self, request):
        articles_list = Article.objects.filter(article_status='published')
        paginator = Paginator(articles_list, 2)
        page = request.GET.get('page')
        try:
            articles = paginator.page(page)
        except PageNotAnInteger:
            articles = paginator.page(1)
        except EmptyPage:
            articles = paginator.page(paginator.num_pages)
        context = {'articles': articles,
                   'page': page}
        return render(request, 'blog/articles/list.html', context)


class ArticleView(View):

    def get(self, request, slug):
        article = get_object_or_404(Article,
                                    slug=slug,
                                    article_status='published')
        context = {'article': article}
        return render(request, 'blog/articles/details.html', context)
