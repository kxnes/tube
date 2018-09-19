from django.contrib import admin
from django.utils.html import format_html_join
from django.utils.safestring import mark_safe

from .models import Keyword, YoutubeVideo


@admin.register(YoutubeVideo)
class YoutubeVideoAdmin(admin.ModelAdmin):
    pass


@admin.register(Keyword)
class KeywordAdmin(admin.ModelAdmin):
    exclude = ('videos', )
    search_fields = ('key_word', )
    readonly_fields = ('videos_inline', )

    def videos_inline(self, obj=None):
        return format_html_join(mark_safe('<br>'), '{}', ((line,) for line in obj.videos.all()))
    videos_inline.short_description = 'Videos'
