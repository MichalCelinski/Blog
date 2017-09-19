from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.urlresolvers import reverse


ARTICLE_STATUS = (
    ('draft', 'draft'),
    ('published', 'published'),
)


class Article(models.Model):
    title = models.CharField(max_length=50)
    slug = models.SlugField(max_length=50, unique_for_date='publish_date')
    author = models.ForeignKey(User, related_name='blog_article')
    article = models.TextField()
    publish_date = models.DateTimeField(default=timezone.now)
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)
    article_status = models.CharField(max_length=20, choices=ARTICLE_STATUS, default='draft')

    class Meta:
        ordering = ('-publish_date',)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog:article_details',
                       args=[self.slug])


