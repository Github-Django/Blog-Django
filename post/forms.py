import django_filters
from .models import adminpost

class ProductFilter(django_filters.FilterSet):
    class Meta:
        model = adminpost
        fields = ['title',
                  'author',
                  'category',
                  'description',
                  'is_special']
