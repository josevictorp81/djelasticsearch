# djelastisearch

Exemplo simples de uma API de artigos, que usa o `elasticsearch` como o motor de de busca para trazer as informações do banco de dados e servir as requisições do tipo GET (listagem dos dados).

Para o uso do elasticsearch como motor de buscar dos dados, necessita-se dos seguintes passos:
- Instalar as seguintes bibliotecas:
```
pip install django-elasticsearch-dsl
pip install django-elasticsearch-dsl-drf
```
- Registrar nos `INSTALED_APPS`:
```PYTHON
INSTALLED_APPS = [
    ...
    'django_elasticsearch_dsl',
    'django_elasticsearch_dsl_drf',
    ...
]
        return self.title
```
- Definir no `settings.py` onde a instancia do elasticsearch está executando:
```python
ELASTICSEARCH_DSL = {
    'default': {
        'hosts': '127.0.0.1:9200'
    },
}
```
- Criar os models:
```python
class Category(models.Model):
    title = models.CharField(max_length=100)

    def __str__(self) -> str:
        return self.title

class Article(models.Model):
    title = models.CharField(max_length=100)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.title
```
- Criar o `documents.py` onde os dados existentes são copiados para o elasticsearch. Para cada modelo que queremos adicionar ao elasticsearch, devemos criar uma classe documento para ele.
```python
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
```
- Criar o `serializers.py`:
```python
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
```
- Criar as views, com o atributo *title* definido como filtro para pesquisa:
```python
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
```
# Executando Aplicação

Neste exemplo, é usado uma instancia do elasticksearch executando em um *container docker*, para instanciá-lo execute o comando abaixo.
```docker
docker run -p 9200:9200 -p 9300:9300 -e "discovery.type=single-node" docker.elastic.co/elasticsearch/elasticsearch:7.14.0
```
- Crie um ambiente virtual e ative
```
python -m venv venv
source /venv/bin/activate (linux)
/venv/script/activate (windows)
```
- Instale as dependências
```
pip install -r requirements.txt
```
- Execute as migrations para o banco de dados
```
python manage.py makemigrations
python manage.py migrate
```
- Popule o banco de dados.
```
python manage.py populate_db
```
- Indexe os dados no elasticsearch:
```
python manage.py search_index --rebuild
```
- Executar aplicação.
```
python manage.py runserver
```
# Endpoints
No browser acesse - 127.0.0.1:8000:
```
/api/ - lista as categorias e artigos usando os recurso providos pelo djangorestframework

/api/es/ - Categorias e artigos listados usando elasticsearch.
```

# Frameworks e Bibliotecas
- [Django](https://www.djangoproject.com/)
- [Django REST Framework](https://www.django-rest-framework.org/)
- [Django Elasticsearch DSL](https://django-elasticsearch-dsl.readthedocs.io/en/latest/)
- [django-elasticsearch-dsl-drf](https://django-elasticsearch-dsl-drf.readthedocs.io/en/latest/)
