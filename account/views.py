from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView
from .models import User
from .forms import ProfileForm
from .mixin import FieldsMixin, FormValidMixin, AuthorAccsesMixin, SuperUserAccsesMixin, AuthorsAccessMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from post.models import adminpost


# Create your views here.


class ArticleList(AuthorsAccessMixin, ListView):
    template_name = 'registration/home.html'

    def get_queryset(self):
        if self.request.user.is_superuser:
            return adminpost.objects.all()
        else:
            return adminpost.objects.filter(author=self.request.user)


class ArticleCreate(AuthorsAccessMixin, FieldsMixin, FormValidMixin, CreateView):
    model = adminpost
    template_name = 'registration/article-create-update.html'


class ArticleUpdate(LoginRequiredMixin, FieldsMixin, FormValidMixin, AuthorAccsesMixin, UpdateView):
    model = adminpost
    template_name = 'registration/article-create-update.html'


class ArticleDelete(SuperUserAccsesMixin, DeleteView):
    model = adminpost
    success_url = reverse_lazy('account:home')
    template_name = "registration/adminpost_confirm_delete.html"


class Profile(LoginRequiredMixin, UpdateView):
    model = User
    form_class = ProfileForm
    template_name = 'registration/profile.html'
    success_url = reverse_lazy('account:profile')

    def get_object(self, queryset=None):
        return User.objects.get(pk=self.request.user.pk)

    def get_form_kwargs(self):
        kwargs = super(Profile, self).get_form_kwargs()
        kwargs.update({
            'user': self.request.user
        })
        return kwargs


class LoginRedirect(LoginView):
    def get_success_url(self):
        user = self.request.user
        if user.is_superuser or user.is_author:
            return reverse_lazy('account:home')
        else:
            return reverse_lazy('account:profile')


from django.http import HttpResponse
from django.shortcuts import render, redirect
from .forms import SignupForm
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.core.mail import EmailMessage


class Register(CreateView):
    form_class = SignupForm
    template_name = 'registration/register.html'

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_active = False
        user.save()
        current_site = get_current_site(self.request)
        mail_subject = 'فعالسازی اکانت'
        message = render_to_string('registration/activate_account.html', {
            'user': user,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': account_activation_token.make_token(user),
        })
        to_email = form.cleaned_data.get('email')
        email = EmailMessage(
            mail_subject, message, to=[to_email]
        )

        email.send()

        return HttpResponse('<a href="/login">ورود</a> لینک فعالسازی به ایمیل شما فرستاده شد  ')

    # def signup(request):
    #     if request.method == 'POST':
    #         form = SignupForm(request.POST)
    #         if form.is_valid():
    #             user = form.save(commit=False)
    #             user.is_active = False
    #             user.save()
    #             current_site = get_current_site(request)
    #             mail_subject = 'Activate your blog account.'
    #             message = render_to_string('acc_active_email.html', {
    #                 'user': user,
    #                 'domain': current_site.domain,
    #                 'uid':urlsafe_base64_encode(force_bytes(user.pk)),
    #                 'token':account_activation_token.make_token(user),
    #             })
    #             to_email = form.cleaned_data.get('email')
    #             email = EmailMessage(
    #                         mail_subject, message, to=[to_email]
    #             )
    #             email.send()
    #             return HttpResponse('Please confirm your email address to complete the registration')
    #     else:
    #         form = SignupForm()
    #     return render(request, 'signup.html', {'form': form})


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()

        return HttpResponse(' اکانت با موفقیت فعال شد برای ورود کلیک کنید <a href="/login">ورود</a>')
    else:
        return HttpResponse('لینک منقضی شده است! برای تلاش دوباره کلیک کنید <a href="/register">ورود</a>')


