from rest_framework import (
    authentication,
    decorators,
    generics,
    mixins,
    permissions,
    renderers,
    response,
    viewsets
)

from .models import Keyword
from .serializers import KeywordSerializer


class KeywordViewSet(mixins.CreateModelMixin, mixins.ListModelMixin, mixins.DestroyModelMixin, viewsets.GenericViewSet):
    queryset = Keyword.objects.all()
    serializer_class = KeywordSerializer

    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    renderer_classes = (renderers.JSONRenderer, )

    # noinspection PyUnusedLocal
    @decorators.action(detail=True, url_path='video')
    def retrieve_videos(self, request, *args, **kwargs):
        keyword = generics.get_object_or_404(self.queryset, pk=kwargs.get('pk'))
        videos = keyword.videos.all()
        return response.Response({
            'key_word': keyword.key_word,
            'id': keyword.pk,
            'urls': [
                'https://www.youtube.com/watch?v='.format(v) for v in keyword.videos.values_list('video_id', flat=True)
            ]
        })
