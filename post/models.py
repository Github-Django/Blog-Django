from django.db import models
from django.urls import reverse
from account.models import User
from django.utils.html import format_html
from django.utils import timezone
from extensions.utils import jalali_converter


# my manager
class ArticleManager(models.Manager):
    def published(self):
        return self.filter(status='p')


class CtegoryManager(models.Manager):
    def active(self):
        return self.filter(status=True)

class Category(models.Model):
    parent = models.ForeignKey('self', default=None, null=True, blank=True, on_delete=models.SET_NULL,
                               related_name='children')
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    status = models.BooleanField(max_length=1)
    position = models.IntegerField()

    class Meta:
        ordering = ['position']

    def __str__(self):
        return self.title

    objects = CtegoryManager()


class IPAddress(models.Model):
    ip_address = models.GenericIPAddressField()


class adminpost(models.Model):
    STATUS_CHOICES = (
        ('d', 'Draft'),
        ('p', 'Published'),
        ('i', 'investigation'),
        ('b', 'back'),
    )
    title = models.CharField(max_length=200)
    author = models.ForeignKey(User, null=True, on_delete=models.SET_NULL, related_name='articles')
    slug = models.SlugField(max_length=200, unique=True)
    category = models.ManyToManyField(Category, related_name="articles")
    description = models.TextField(Category)
    thumbnail = models.ImageField(upload_to='imagess', default='#', blank=True, null=True)
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    is_special = models.BooleanField(default=False)
    status = models.CharField(max_length=1, choices=STATUS_CHOICES)
    hits = models.ManyToManyField(IPAddress, through='ArticleHit', blank=True, related_name='hits')

    def __str__(self):
        return self.title

    def jpublish(self):
        return jalali_converter(self.publish)

    def get_absolute_url(self):
        return reverse('account:home')

    def thumbnail_tag(self):
        return format_html("<img width=90 height=60 style='border-radius:5px;' src='{}'>".format(self.thumbnail.url))

    def category_to_str(self):
        return ', '.join([category.title for category in self.category.active()])

    objects = ArticleManager()


class ArticleHit(models.Model):
    article = models.ForeignKey(adminpost, on_delete=models.CASCADE)
    ip_address = models.ForeignKey(IPAddress, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
