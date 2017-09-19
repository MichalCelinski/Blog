from .models import Article, Comment
from django.shortcuts import render, get_object_or_404
from django.views import View
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from .forms import CommentArticleForm, EmailArticleForm
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
        article = get_object_or_404(Article, slug=slug)
        comments = article.comments.filter(active=True)
        context = {'article': article,
                   'comments': comments}
        return render(request, 'blog/articles/details.html', context)


class ArticleCommentView(View):

    def get(self, request, article_id):
        article = get_object_or_404(Article, pk=article_id)
        comment_form = CommentArticleForm()
        context = {'article': article,
                   'comment_form': comment_form}
        return render(request, 'blog/articles/comment.html', context)

    def post(self, request, article_id):
        article = get_object_or_404(Article, pk=article_id)
        article_url = request.build_absolute_uri(article.get_absolute_url())
        comment_form = CommentArticleForm(request.POST)
        added = False
        if comment_form.is_valid():
            cleaned_data = comment_form.cleaned_data
            new_comment = Comment()
            new_comment.name = cleaned_data['name']
            new_comment.email = cleaned_data['email']
            new_comment.comment = cleaned_data['comment']
            new_comment.article = article
            new_comment.save()
            added = True
        context = {'added': added, 'article_url': article_url}
        return render(request, 'blog/articles/comment.html', context)


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
        context = {'sent': sent, 'article_url': article_url}
        return render(request, 'blog/articles/share.html', context)
