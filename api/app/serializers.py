from rest_framework import serializers
from .models import Authors, WordsPerAuthor

class AuthorsSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Authors
        fields = ('author_id', 'author_name')

class WordsPerAuthorSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = WordsPerAuthor
        fields = ('author_id', 'word', 'word_count')
