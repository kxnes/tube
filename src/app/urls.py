from django.urls import path, include

from rest_framework.authtoken.views import obtain_auth_token
from rest_framework.routers import DefaultRouter

from .views import KeywordViewSet


router = DefaultRouter()
router.register('', KeywordViewSet)

urlpatterns = [
    path('auth/', obtain_auth_token),
    path('words/', include(router.urls))
]
