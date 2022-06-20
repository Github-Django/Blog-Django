from django.http import Http404
from django.shortcuts import get_object_or_404, redirect
from post.models import adminpost

class FieldsMixin():
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_superuser:
            self.fields = ["title", "author", "slug", "category", "description", "thumbnail", "publish", 'is_special',
                           "status"]
        elif request.user.is_author:
            self.fields = ["title", "slug", "category", "description", "thumbnail", "is_special", "publish"]
        else:
            raise Http404('you cant see this page')
        return super().dispatch(request, *args, **kwargs)


class FormValidMixin():
    def form_valid(self, form):
        if self.request.user.is_superuser:
            form.save()
        else:
            self.obj = form.save(commit=False)
            self.obj.author = self.request.user
            self.obj.status = 'd'
        return super().form_valid(form)


class AuthorAccsesMixin():
    def dispatch(self, request, pk, *args, **kwargs):
        article = get_object_or_404(adminpost, pk=pk)
        if article.author == request.user and article.status in ['b', 'd'] or request.user.is_superuser:
            return super().dispatch(request, *args, **kwargs)
        else:
            raise Http404('you cant see this page')


class AuthorsAccessMixin():
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            if request.user.is_superuser or request.user.is_author:
                return super().dispatch(request, *args, **kwargs)
            else:
                return redirect('account:profile')
        else:
            return redirect('login')


class SuperUserAccsesMixin():
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_superuser:
            return super().dispatch(request, *args, **kwargs)
        else:
            raise Http404('you cant see this page')
