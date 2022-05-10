from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register('article-search', views.ArticleDocumentView, basename='article-search')
router.register('category-search', views.CategoryDocumentView, basename='category-search')

urlpatterns = [
    path('', include(router.urls))
]