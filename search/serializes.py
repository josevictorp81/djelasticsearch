from django_elasticsearch_dsl_drf.serializers import DocumentSerializer

from search.documents import ArticleDocument, CategoryDocument


class ArticleDocumentSerializer(DocumentSerializer):
    class Meta:
        document = ArticleDocument
        fields = '__all__'


class CategoryDocumentSerializer(DocumentSerializer):
    class Meta:
        document = CategoryDocument
        fields = '__all__'
        