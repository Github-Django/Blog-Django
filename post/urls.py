from django.urls import path
from . import views


app_name = 'post'
urlpatterns = [
    path('', views.ArticleList.as_view(), name='home'),
    path('page/<int:page>', views.ArticleList.as_view(), name='home'),
    path('article/<slug:slug>/', views.ArticleDetail.as_view(), name="detail"),
    path('preview/<int:pk>', views.ArticlePreview.as_view(), name="preview"),
    path('category/<slug:slug>/', views.CategoryList.as_view(), name="category"),
    path('category/<slug:slug>/page/<int:page>', views.CategoryList.as_view(), name="category"),
    path('author/<slug:username>/', views.AuthorList.as_view(), name="author"),
    path('author/<slug:username>/page/<int:page>', views.AuthorList.as_view(), name="author"),
    path('search/', views.SearchList.as_view(), name="search"),
    path('search/page/<int:page>', views.SearchList.as_view(), name="search"),
    path('list/', views.ProductFilter, name="product-list"),

]

from django.conf import settings
from django.conf.urls.static import static

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

