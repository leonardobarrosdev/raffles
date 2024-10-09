from django.db import models


class MediaContent(models.Model):
    domain = models.SlugField(max_length=255, null=True, blank=True)
    google_tag_manage_id = models.CharField(max_length=255, null=True, blank=True)
    pixel_facebook = models.CharField(max_length=255, null=True, blank=True)
    youtube_video_link = models.CharField(max_length=255, null=True, blank=True)
