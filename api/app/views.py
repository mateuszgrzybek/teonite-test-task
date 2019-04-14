from django.shortcuts import render
from rest_framework import viewsets
from .models import Authors
from .serializers import AuthorsSerializer

class AuthorsView(viewsets.ModelViewSet):
    queryset = Authors.objects.all()
    serializer_class = AuthorsSerializer
