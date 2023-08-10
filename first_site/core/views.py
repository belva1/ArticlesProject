from django.contrib import messages
from django.shortcuts import render, redirect
from .models import Articles
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView
from .forms import ArticleForm
from django.urls import reverse, reverse_lazy


class CustomSuccessMessageMixin:
    @property
    def success_msg(self):
        return False

    def form_valid(self, form):
        messages.success(self.request, self.success_msg)
        return super().form_valid(form)


class HomeListView(ListView):
    model = Articles
    template_name = 'index.html'
    context_object_name = 'list_articles'


class HomeDetailView(DetailView):
    model = Articles
    template_name = 'detail.html'
    context_object_name = 'get_article'


class ArticleCreateView(CustomSuccessMessageMixin, CreateView):
    model = Articles
    template_name = 'edit_page.html'
    form_class = ArticleForm
    success_url = reverse_lazy('edit_page')
    success_msg = 'Article was created successfully.'

    def get_context_data(self, **kwargs):
        kwargs['list_articles'] = Articles.objects.all().order_by('-id')
        return super().get_context_data(**kwargs)


class ArticleUpdateView(CustomSuccessMessageMixin, UpdateView):
    model = Articles
    template_name = 'edit_page.html'
    form_class = ArticleForm
    success_url = reverse_lazy('edit_page')
    success_msg = 'Article was updated successfully.'

    def get_context_data(self, **kwargs):
        kwargs['update'] = True
        return super().get_context_data(**kwargs)


class ArticleDeleteView(DeleteView):
    model = Articles
    template_name = 'edit_page.html'
    success_url = reverse_lazy('edit_page')
    success_msg = 'Article was deleted successfully.'

    def post(self, request, *args, **kwargs):
        messages.success(self.request, self.success_msg)
        return super().post(request)