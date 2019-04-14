from rest_framework import serializers
from .models import Authors

class AuthorsSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Authors
        fields = ('author_id', 'author_name')
