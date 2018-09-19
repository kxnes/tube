from django.db import models


class YoutubeVideo(models.Model):
    video_id = models.CharField(verbose_name='Video ID', max_length=128)

    class Meta:
        ordering = ('video_id', )

    def __str__(self):
        return self.video_id


class Keyword(models.Model):
    key_word = models.CharField(max_length=128, verbose_name='Keyword', unique=True)
    videos = models.ManyToManyField(to='YoutubeVideo', related_name='keyboards', verbose_name='YouTube video')

    class Meta:
        ordering = ('key_word', )

    def __str__(self):
        return self.key_word
