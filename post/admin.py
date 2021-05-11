from django.contrib import admin
from .models import adminpost, Category, IPAddress
from account.models import User


# Create your actions here.
def make_published(modeladmin, request, queryset):
    rows_updated = queryset.update(status='p')
    if rows_updated == 1:
        message_bit = 'is publish'
    else:
        message_bit = 'is published'
    modeladmin.message_user(request, "{} article {}".format(rows_updated, message_bit))


make_published.short_description = "selected is published"


def make_draft(modeladmin, request, queryset):
    rows_updated = queryset.update(status='d')
    if rows_updated == 1:
        message_bit = 'is draft'
    else:
        message_bit = 'is drafted'
    modeladmin.message_user(request, "{} article {}".format(rows_updated, message_bit))


make_draft.short_description = "selected is drafted"


def make_published_category(modelcategory, request, queryset):
    rows_updated = queryset.update(status=True)
    if rows_updated == 1:
        message_bit = 'is publish'
    else:
        message_bit = 'is published'
    modelcategory.message_user(request, "{} category {}".format(rows_updated, message_bit))


make_published.short_description = "selected is published"


def make_draft_category(modelcategory, request, queryset):
    rows_updated = queryset.update(status=False)
    if rows_updated == 1:
        message_bit = 'is draft'
    else:
        message_bit = 'is drafted'
    modelcategory.message_user(request, "{} category {}".format(rows_updated, message_bit))


make_draft.short_description = "selected is drafted"


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('position', 'title', 'slug', 'parent', 'status')
    list_filter = (['status'])
    search_fields = ('title', 'slug')
    prepopulated_fields = {'slug': ('title',)}  # title va slug ba ham set mishan
    actions = [make_published_category, make_draft_category]


admin.site.register(Category, CategoryAdmin)


class RadifAdmin(admin.ModelAdmin):

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "author":
            kwargs['queryset'] = User.objects.filter(is_staff=True)
            return super().formfield_for_foreignkey(db_field, request, **kwargs)

    list_display = ('title', 'thumbnail_tag', 'slug', 'author', 'jpublish', 'is_special', 'status', 'category_to_str')
    list_filter = ('publish', 'status')
    search_fields = ('title', 'description')
    ordering = ('-publish', '-status')
    actions = [make_published, make_draft]

    # def category_to_str(self, obj):
    #     return ', '.join([category.title for category in obj.category.active()])


# Register your models here.
admin.site.register(adminpost, RadifAdmin)
admin.site.register(IPAddress)
