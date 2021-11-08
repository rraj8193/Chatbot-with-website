from django.shortcuts import render
from article.owner import OwnerCreateView,OwnerDeleteView,OwnerDetailView,OwnerListView,OwnerUpdateView
from article.models import Article
# Create your views here.

class ArticleListView(OwnerListView):
    model = Article

class ArticleDetailView(OwnerDetailView):
    model = Article

class ArticleCreateView(OwnerCreateView):
    model = Article
    fields = ['title','text']


class ArticleUpdateView(OwnerUpdateView):
    model = Article
    fields = ['title','text']

class ArticleDeleteView(OwnerDeleteView):
    model = Article