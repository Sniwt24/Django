from django.forms import SelectDateWidget
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView

from blogapp.forms import CreateArticleForm
from blogapp.models import Article, Tag, Author, Category


# Create your views here.
class ArticleListView(ListView):
    template_name = "blogapp/article_list.html"
    queryset = Article.objects.defer("content").select_related("author").defer("author__bio").select_related("category").prefetch_related("tags")


class CreateArticleView(CreateView):
    model = Article
    form_class = CreateArticleForm
    success_url = reverse_lazy("blogapp:article_list")


class CreateTagView(CreateView):
    model = Tag
    fields = "name",
    success_url = reverse_lazy("blogapp:article_list")


class CreateAuthorView(CreateView):
    model = Author
    fields = "name", "bio"
    success_url = reverse_lazy("blogapp:article_list")


class CreateCategoryView(CreateView):
    model = Category
    fields = "name",
    success_url = reverse_lazy("blogapp:article_list")