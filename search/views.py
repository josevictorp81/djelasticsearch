from django_elasticsearch_dsl_drf.filter_backends import SearchFilterBackend
from django_elasticsearch_dsl_drf.viewsets import DocumentViewSet

from .documents import ArticleDocument, CategoryDocument
from .serializes import ArticleDocumentSerializer, CategoryDocumentSerializer

class ArticleDocumentView(DocumentViewSet):
    document = ArticleDocument
    serializer_class = ArticleDocumentSerializer

    filter_backends = [
        SearchFilterBackend
    ]

    search_fields = (
        'title',
    )


class CategoryDocumentView(DocumentViewSet):
    document = CategoryDocument
    serializer_class = CategoryDocumentSerializer

    filter_backends = [
        SearchFilterBackend
    ]

    search_fields = (
        'title',
    )
