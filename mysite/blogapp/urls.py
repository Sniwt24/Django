from django.urls import path
from .views import ArticleListView, CreateArticleView, CreateTagView, CreateAuthorView, CreateCategoryView

app_name = "blogapp"

urlpatterns = [
    path("", ArticleListView.as_view(), name="article_list"),
    path("create/", CreateArticleView.as_view(), name="article_create"),
    path("tag/create/", CreateTagView.as_view(), name="tag_create"),
    path("author/create/", CreateAuthorView.as_view(), name="author_create"),
    path("category/create/", CreateCategoryView.as_view(), name="category_create"),
]