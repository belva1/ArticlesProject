from django.contrib import messages
from django.contrib.auth.views import LoginView, LogoutView
from .models import Articles
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView
from .forms import ArticleForm, AuthUserForm, RegisterUserForm
from django.urls import reverse_lazy
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin, AccessMixin
from django.http import HttpResponseRedirect


class CustomSuccessMessageMixin:
    @property
    def success_msg(self):
        return False

    def form_valid(self, form):
        messages.success(self.request, self.success_msg)
        return super().form_valid(form)


class LoginRequiredMixin(AccessMixin):
    """Verify that the current user is authenticated."""

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)


class ProjectLoginView(LoginView):
    template_name = 'login_page.html'
    form_class = AuthUserForm
    success_url = reverse_lazy('home')

    def get_success_url(self):
        return self.success_url


class ProjectRegisterView(CreateView):
    model = User
    template_name = 'register_page.html'
    form_class = RegisterUserForm
    success_url = reverse_lazy('home')
    success_msg = 'User was created successfully.'

    #  Below is a method that provides automatic authorization upon successful registration.
    def form_valid(self, form):
        form_valid = super().form_valid(form)
        username = form.cleaned_data["username"]
        password = form.cleaned_data["password"]
        auth_user = authenticate(username=username, password=password)
        login(self.request, auth_user)
        return form_valid


class ProjectLogoutView(LogoutView):
    next_page = reverse_lazy('home')


class HomeListView(ListView):
    model = Articles
    template_name = 'index.html'
    context_object_name = 'list_articles'


class HomeDetailView(DetailView):
    model = Articles
    template_name = 'detail_page.html'
    context_object_name = 'get_article'


class ArticleCreateView(CustomSuccessMessageMixin, LoginRequiredMixin, CreateView):
    model = Articles
    template_name = 'article_functionality_page.html'
    form_class = ArticleForm
    success_url = reverse_lazy('edit_page')
    success_msg = 'Article was created successfully.'

    def get_context_data(self, **kwargs):
        kwargs['list_articles'] = Articles.objects.all().order_by('-id')
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.author = self.request.user
        self.object.save()
        return super().form_valid(form)


class ArticleUpdateView(CustomSuccessMessageMixin, LoginRequiredMixin, UpdateView):
    model = Articles
    template_name = 'article_functionality_page.html'
    form_class = ArticleForm
    success_url = reverse_lazy('edit_page')
    success_msg = 'Article was updated successfully.'

    def get_context_data(self, **kwargs):
        kwargs['update'] = True
        return super().get_context_data(**kwargs)

    def get_form_kwargs(self):
        """Return the keyword arguments for instantiating the form."""
        kwargs = super().get_form_kwargs()

        """
        AUTHOR OF EDITED ARTICLE:
        print(kwargs['instance'].author)
        
        CURRENT AUTHENTICATED USER:
        print(self.request.user)
        """

        if self.request.user != kwargs['instance'].author:
            return self.handle_no_permission()
        return kwargs


class ArticleDeleteView(DeleteView, LoginRequiredMixin):
    model = Articles
    template_name = 'article_functionality_page.html'
    success_url = reverse_lazy('edit_page')
    success_msg = 'Article was deleted successfully.'

    def post(self, request, *args, **kwargs):
        messages.success(self.request, self.success_msg)
        return super().post(request)

    def form_valid(self, request, *args, **kwargs):
        """
        Call the delete() method on the fetched object and then redirect to the
        success URL.
        """
        self.object = self.get_object()

        """
        AUTHOR OF DELETED ARTICLE:
        print(self.object.author)

        CURRENT AUTHENTICATED USER:
        print(self.request.user)
        """

        if self.request.user != self.object.author:
            return self.handle_no_permission()

        success_url = self.get_success_url()
        self.object.delete()
        return HttpResponseRedirect(success_url)