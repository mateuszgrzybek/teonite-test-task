from rest_framework import serializers
from .models import Authors, WordsPerAuthor, TotalWords


class AuthorsSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Authors
        fields = ('author_id', 'author_name')


class TotalWordsSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = TotalWords
        fields = ('word', 'word_count')


class WordsPerAuthorSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = WordsPerAuthor
        fields = ('author_id', 'word', 'word_count')
