from rest_framework import viewsets
from rest_framework.mixins import ListModelMixin

from core.models import Category, Article
from .serializers import ArticleSerializers, CategorySerializers


class CategoryViewset(ListModelMixin, viewsets.GenericViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializers


class ArticleViewset(ListModelMixin, viewsets.GenericViewSet):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializers
