from django_elasticsearch_dsl import Document, fields
from django_elasticsearch_dsl.registries import registry

from core.models import Article, Category

@registry.register_document
class CategoryDocument(Document):
    id = fields.IntegerField()
    
    class Index:
        name = 'categories'
        settings = {'number_of_shards': 1, 'number_of_replicas': 0}

    class Django:
        model = Category
        fields = ['title']


@registry.register_document
class ArticleDocument(Document):
    category = fields.ObjectField(
        attr='category',
        properties={
            'id': fields.IntegerField(),
            'title': fields.TextField(
                attr='title',
                fields={
                    'raw': fields.KeywordField(),
                }
            )
        }
    )

    class Index:
        name = 'articles'
        settings = {'number_of_shards': 1, 'number_of_replicas': 0}

    class Django:
        model = Article
        fields = ['title']
