from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

# Register your models here.

UserAdmin.fieldsets += (

    ('fields special user', {'fields': ('is_author', 'special_user')}),
)
UserAdmin.list_display += (
    "is_author", "is_special_user"
)
admin.site.register(User, UserAdmin)
