import celery
import requests

from django.conf import settings
from django.core import exceptions

from .models import Keyword, YoutubeVideo


try:
    API_KEY = settings.YOUTUBE_API_KEY
except AttributeError:
    raise exceptions.ImproperlyConfigured('`YOUTUBE_API_KEY` is not set in `local.py` settings.')


SEARCH_URL = 'https://www.googleapis.com/youtube/v3/search'
SEARCH_PARAMS = {
    'maxResults': '5',
    'part': 'snippet',
    'fields': 'items/id/videoId',
    'key': API_KEY,
}


@celery.task()
def search_videos():
    try:
        for kw in Keyword.objects.all():
            # get new videos by keyword
            response = requests.get(SEARCH_URL, params={'q': kw.key_word, **SEARCH_PARAMS})

            if response.status_code != 200:
                raise Exception(
                    '`YOUTUBE_API_KEY` is invalid or check youtube api response: {}'.format(response.json())
                )

            received_videos = set(i['id']['videoId'] for i in response.json()['items'])

            # check existing videos in db
            existing_videos = set(kw.videos.values_list('video_id', flat=True))

            # this video ids are not in db
            append_videos = received_videos - existing_videos

            # 2 db requests, because `bulk_create` returns object ids only for `postgresql` backend,
            # for other backend returns None and in `add` method will be Exception:
            #    ValueError: instance is on database "None", value is on database "default"

            # 1 step: create new videos
            kw.videos.bulk_create([YoutubeVideo(video_id=vid) for vid in append_videos])
            # 2 step: get new videos with ids
            videos = YoutubeVideo.objects.filter(video_id__in=append_videos)
            # 3 step: update relation with keyword
            kw.videos.add(*videos)
    except Exception as exc:
        raise Exception('Exception occurred, need RND') from exc
    finally:
        print('Done!')
