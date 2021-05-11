from django import template
from ..models import Category, adminpost
from django.db.models import Count, Q
from django.utils import timezone

register = template.Library()


@register.simple_tag
def title():
    return 'وبلاگ جنگویی'


@register.inclusion_tag('one/partials/category_navbar.html')
def category_navbar():
    return {
        "category": Category.objects.filter(status=True)
    }


@register.inclusion_tag('one/partials/popular_articles.html')
def popular_articles():
    last_month = timezone.datetime.today() - timezone.timedelta(days=30)
    return {
        "popular_articles": adminpost.objects.published().annotate(
            count=Count('hits', filter=Q(articlehit__created__gt=last_month))
        ).order_by('-count', '-publish')[:5]
    }
