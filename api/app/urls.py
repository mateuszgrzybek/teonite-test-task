from django.urls import path, include
from .views import AuthorsView, WordsPerAuthorView, TotalWordsView
from rest_framework import routers

router = routers.DefaultRouter()
# router.register('authors', AuthorsView)

urlpatterns = [
    path('', include(router.urls)),
    path('authors/', AuthorsView.as_view(), name='authors'),
    path('stats/', TotalWordsView.as_view(), name='total_words'),
    path('stats/<str:author_id>/', WordsPerAuthorView.as_view(),
         name='words_per_author'),
]
