from django.views.generic import ListView, DetailView
from account.models import User
from account.mixin import AuthorAccsesMixin
from django.shortcuts import render, get_object_or_404
from .models import adminpost, Category
from django.db.models import Q
from django.contrib.auth import logout
from django.urls import reverse_lazy
from .forms import ProductFilter

class ArticleList(ListView):
    template_name = 'one/home.html'
    paginate_by = 4
    queryset = adminpost.objects.published().order_by('publish')

class ArticleDetail(DetailView):
    template_name = 'one/detail.html'

    def get_object(self, queryset=None):
        slug = self.kwargs.get('slug')
        article = get_object_or_404(adminpost.objects.published(),
                                    slug=slug,
                                    # pk=self.kwargs.get('pk')
                                    )
        ip_address = self.request.user.ip_address
        if ip_address not in article.hits.all():
            article.hits.add(ip_address)

        return article

class ArticlePreview(AuthorAccsesMixin, DetailView):
    template_name = 'one/detail.html'
    context_object_name = 'article'

    def get_object(self, queryset=None):
        pk = self.kwargs.get('pk')
        return get_object_or_404(adminpost, pk=pk)

class CategoryList(ListView):
    paginate_by = 4
    template_name = 'one/category.html'

    def get_queryset(self):
        global category
        slug = self.kwargs.get('slug')
        category = get_object_or_404(Category, slug=slug, status=True)
        return adminpost.objects.published()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = category
        return context

class AuthorList(ListView):
    paginate_by = 3
    template_name = 'one/author_list.html'

    def get_queryset(self):
        global author
        username = self.kwargs.get('username')
        author = get_object_or_404(User, username=username)
        return author.articles.published()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['author'] = author
        return context

class SearchList(ListView):
    paginate_by = 3
    template_name = 'one/search_list.html'

    def get_queryset(self):
        search = self.request.GET.get('q')
        return adminpost.objects.filter(Q(description__icontains=search) | Q(title__icontains=search))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search'] = self.request.GET.get('q')
        return context

def logoutView(request):
    logout(request)
    return reverse_lazy(request.GET.get('next'))

def product_list(request):
    filter = ProductFilter(request.GET, queryset=adminpost.objects.all())
    return render(request, '', {'filter': filter})