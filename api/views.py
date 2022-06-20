from django.contrib.auth import get_user_model
from post.models import adminpost
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .permissions import IsSuperUserOrStaffReadOnly, IsStaffOrReadOnly, IsAuthorOrReadOnly
from .serializers import ArticleSerializers, UserSerializers
from rest_framework import viewsets

class ListViewSet(viewsets.ModelViewSet):
    queryset = adminpost.objects.all()
    serializer_class = ArticleSerializers
    filter_fields = ['status', 'author__username']
    search_fields = ['title', 'author__username', 'description']
    ordering_fields = ['status', 'publish']
    ordering = ["-publish"]
    def get_permissions(self):
        if self.action in ['list']:
            permission_classes = [IsAuthenticatedOrReadOnly]
        else:
            permission_classes = [IsStaffOrReadOnly, IsAuthorOrReadOnly,IsSuperUserOrStaffReadOnly]
        return [permission() for permission in permission_classes]

class UserViewSet(viewsets.ModelViewSet):
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializers
    permission_classes = [IsSuperUserOrStaffReadOnly]