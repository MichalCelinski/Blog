from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^$', views.ArticlesListView.as_view(), name='articles_list'),
    url(r'^(?P<slug>(\S)+)$',
        views.ArticleView.as_view(), name='slug')
]