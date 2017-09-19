from .models import Article
from django.shortcuts import render, get_object_or_404
from django.views import View
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from .forms import EmailArticleForm
from .services import send_article


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
        context = {'articles': articles}
        return render(request, 'blog/articles/list.html', context)


class ArticleView(View):

    def get(self, request, slug):
        article = get_object_or_404(Article,
                                    slug=slug,
                                    article_status='published')
        context = {'article': article}
        return render(request, 'blog/articles/details.html', context)


class ArticleShareView(View):

    def get(self, request, article_id):
        article = get_object_or_404(Article, pk=article_id)
        form = EmailArticleForm()
        context = {'article': article, 'form': form}
        return render(request, 'blog/articles/share.html', context)

    def post(self, request, article_id):
        article = get_object_or_404(Article, pk=article_id)
        article_url = request.build_absolute_uri(article.get_absolute_url())
        form = EmailArticleForm(request.POST)
        sent = False
        if form.is_valid():
            sent = send_article(article, form, article_url)
        context = {'sent': sent}
        return render(request, 'blog/articles/share.html', context)
