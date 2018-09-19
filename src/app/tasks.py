import celery
import requests

from urllib.parse import urlencode

from django.conf import settings
from django.core import exceptions

from .models import Keyword, YoutubeVideo


try:
    API_KEY = settings.YOUTUBE_API_KEY
except AttributeError as exc:
    raise exceptions.ImproperlyConfigured(
        '`YOUTUBE_API_KEY` is not set in `local.py` settings.'
    ) from exc


SEARCH_URL = 'https://www.googleapis.com/youtube/v3/search?'
SEARCH_PARAMS = {
    'maxResults': '5',
    'part': 'snippet',
    'fields': 'items/id/videoId',
    'key': API_KEY,
}
API = SEARCH_URL + urlencode(SEARCH_PARAMS)


@celery.task()
def search_videos():
    # noinspection PyShadowingNames
    try:
        for kw in Keyword.objects.all():
            # get new videos by keyword
            response = requests.get(API + '&' + urlencode({'q': kw.key_word}))
            received_videos = set(i['id']['videoId'] for i in response.json()['items'])

            # check existing videos in db
            exist_videos = set(kw.videos.values_list('video_id', flat=True))

            # add only new videos
            videos = kw.videos.bulk_create([YoutubeVideo(video_id=vid) for vid in received_videos - exist_videos])
            kw.videos.add(*videos)
    except Exception as exc:
        raise Exception('Exception in search_videos tasks, need RND') from exc
