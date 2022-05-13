from accounts.models import User
from django_elasticsearch_dsl import Document, fields
from django_elasticsearch_dsl.registries import registry

from posts.models import Post


@registry.register_document
class PostDocument(Document):
    post = fields.ObjectField(properties={
        'body':fields.TextField(),
        'slug':fields.TextField(),
    })
    class Index:
        name = 'post'
        settings = {
            'number_of_shards': 1,
            'number_of_replicas': 0,
        }

    class Django:
        model = Post
        fields = [
            'body',
            'slug',            
           
        ]