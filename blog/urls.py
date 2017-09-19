from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^(?P<article_id>\d+)/share/$', views.ArticleShareView.as_view(), name='article_share'),
    url(r'^(?P<article_id>\d+)/comment/$', views.ArticleCommentView.as_view(), name='article_comment'),
    url(r'^(?P<slug>(\S)+)$', views.ArticleView.as_view(), name='article_details'),
    url(r'^$', views.ArticlesListView.as_view(), name='articles_list'),
]