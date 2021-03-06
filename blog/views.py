from .models import Article, Comment
from django.shortcuts import render, get_object_or_404
from django.views import View
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from .forms import CommentArticleForm, EmailArticleForm
from .services import send_article
from taggit.models import Tag
from django.db.models import Count


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


class ArticlesListbyTagView(View):

    def get(self, request, tag_slug):
        tag = get_object_or_404(Tag, slug=tag_slug)
        articles_list = Article.objects.filter(article_status='published', tags__in=[tag])
        paginator = Paginator(articles_list, 2)
        page = request.GET.get('page')
        try:
            articles = paginator.page(page)
        except PageNotAnInteger:
            articles = paginator.page(1)
        except EmptyPage:
            articles = paginator.page(paginator.num_pages)
        context = {'articles': articles, 'tag': tag}
        return render(request, 'blog/articles/list.html', context)


class ArticleView(View):

    def get(self, request, slug):
        article = get_object_or_404(Article, slug=slug)
        comments = article.comments.filter(active=True)
        article_tags_ids = article.tags.values_list('id', flat=True)
        similar_articles = Article.objects.filter(tags__in=article_tags_ids).exclude(id=article.id)
        similar_articles = similar_articles.annotate(same_tags=Count('tags')).order_by('-same_tags', '-publish_date')[:2]
        context = {'article': article,
                   'comments': comments,
                   'similar_articles': similar_articles}
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
            new_comment = Comment.objects.create(name=cleaned_data['name'],
                                                 email=cleaned_data['email'],
                                                 comment=cleaned_data['comment'],
                                                 article=article)
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
