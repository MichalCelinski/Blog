from django.shortcuts import render, get_object_or_404
from django.views import View
from .models import Article
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from .forms import EmailArticleForm
from myblog.local_settings import EMAIL_HOST_USER, EMAIL_HOST_PASSWORD
import smtplib
from email.mime.text import MIMEText


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


def article_share(request, article_id):
    article = get_object_or_404(Article, pk=article_id)
    sent = False
    if request.method == 'POST':
        form = EmailArticleForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            article_url = request.build_absolute_uri(article.get_absolute_url())
            message = MIMEText(u'Przeczytaj <a href="{}">{}</a><br>dodatkowa wiadomość: {}'
                               .format(article_url, article_url, cd['message']), 'html')
            message['Subject'] = '{} zaprasza do lektury "{}"'.format(cd['sender'], article)
            message['From'] = cd['sender']
            message['To'] = cd['email_receiver']
            smtp_server = smtplib.SMTP('smtp.gmail.com:587')
            smtp_server.ehlo()
            smtp_server.starttls()
            smtp_server.ehlo()
            smtp_server.login(EMAIL_HOST_USER, EMAIL_HOST_PASSWORD)
            smtp_server.sendmail(EMAIL_HOST_USER, cd['email_receiver'], message.as_string())
            smtp_server.quit()
            sent = True
    else:
        form = EmailArticleForm()
    return render(request, 'blog/articles/share.html', {'article': article, 'form': form, 'sent': sent})

