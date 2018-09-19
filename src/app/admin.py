from django.contrib import admin

from .models import Keyword, YoutubeVideo


@admin.register(YoutubeVideo)
class YoutubeVideoAdmin(admin.ModelAdmin):
    pass


class VideoInline(admin.TabularInline):
    model = Keyword.videos.through
    extra = 0


@admin.register(Keyword)
class KeywordAdmin(admin.ModelAdmin):
    inlines = (VideoInline, )
    exclude = ('videos', )
    search_fields = ('key_word', )
