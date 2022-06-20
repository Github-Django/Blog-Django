from rest_framework import serializers
from django.contrib.auth import get_user_model
from post.models import adminpost
from drf_dynamic_fields import DynamicFieldsMixin

class ArticleSerializers(DynamicFieldsMixin,serializers.ModelSerializer):

    def get_author(self, obj):
        return obj.author.username

    author = serializers.SerializerMethodField('get_author')

    def validate_title(self, value):
        filter_list = ['php', 'laravel', 'wordpress']
        for i in filter_list:
            if i in value:
                raise serializers.ValidationError(
                    'very very bad world! change languege programmer and say hello world Django')

    class Meta:
        model = adminpost
        # fields = "__all__"
        exclude = ("description", "category", "hits")


class UserSerializers(serializers.ModelSerializer):
    def validate_name(self, value):
        if value == 'admin':
            raise serializers.ValidationError('can not be admin')

    class Meta:
        model = get_user_model()
        fields = "__all__"
