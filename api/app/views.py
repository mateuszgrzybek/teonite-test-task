from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.generics import ListAPIView
from .models import Authors, WordsPerAuthor
from .serializers import AuthorsSerializer, WordsPerAuthorSerializer

class AuthorsView(ListAPIView):
    """View for listing author_id: author_name pairs."""
    serializer_class = AuthorsSerializer

    def get_queryset(self):
        return Authors.objects.all()

    def get(self, request):
        queryset = self.get_queryset()
        serialized_data = AuthorsSerializer(queryset, many=True).data
        authors_json = dict()
        for author in serialized_data:
            authors_json[author['author_id']] = author['author_name']

        return Response(authors_json)

class WordsPerAuthorView(ListAPIView):
    serializer_class = WordsPerAuthorSerializer

    def get_queryset(self, *args, **kwargs):
        return WordsPerAuthor.objects.filter(author_id=self.kwargs['author_id'])

    def get(self, *args, **kwargs):
        queryset = self.get_queryset()
        serialized_data = self.serializer_class(queryset, many=True).data
        words_per_author_json = dict()
        for stats in serialized_data:
            words_per_author_json[stats['word']] = stats['word_count']

        return Response(words_per_author_json)
