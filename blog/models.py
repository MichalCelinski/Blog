from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.urlresolvers import reverse
from taggit.managers import TaggableManager
from tinymce.models import HTMLField


ARTICLE_STATUS = (
    ('draft', 'draft'),
    ('published', 'published'),
)


class Article(models.Model):
    title = models.CharField(max_length=50)
    slug = models.SlugField(max_length=50, unique_for_date='publish_date')
    author = models.ForeignKey(User, related_name='blog_article')
    article = HTMLField()
    publish_date = models.DateTimeField(default=timezone.now)
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)
    article_status = models.CharField(max_length=20, choices=ARTICLE_STATUS, default='draft')
    tags = TaggableManager()

    class Meta:
        ordering = ('-publish_date',)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog:article_details',
                       args=[self.slug])


class Comment(models.Model):
    article = models.ForeignKey(Article, related_name='comments')
    name = models.CharField(max_length=80)
    email = models.EmailField()
    comment = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return 'Komentarz {} do artykułu {}'.format(self.comment, self.article)
