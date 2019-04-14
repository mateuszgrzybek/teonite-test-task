from django.urls import path, include
from .views import AuthorsView
from rest_framework import routers

router = routers.DefaultRouter()
router.register('authors', AuthorsView)

urlpatterns = [
    path('', include(router.urls)),
    # path('authors/', include(AuthorsView.as_view(), name='authors')
]
