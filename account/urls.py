from . import views
from django.urls import path

app_name = "account"

urlpatterns = [
    path('', views.ArticleList.as_view(), name='home'),
    path('article/create', views.ArticleCreate.as_view(), name='article-create'),
    path('article/update/<int:pk>', views.ArticleUpdate.as_view(), name='article-update'),
    path('article/delete/<int:pk>', views.ArticleDelete.as_view(), name='article-delete'),
    path('profile/', views.Profile.as_view(), name='profile'),

]
