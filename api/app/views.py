from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.generics import ListAPIView
from .models import Authors
from .serializers import AuthorsSerializer

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
