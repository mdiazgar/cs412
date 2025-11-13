from django.db import models
# File: dadjokes/models.py
# Author: María Díaz Garrido
# Description: Database models for the dadjokes app. Defines the Joke model
#              with text, contributos, created_at and the Picture model with image_url,
#              name of contributor and timestamp.

# Create your models here.

from django.db import models
from django.utils import timezone

class Joke(models.Model):
    text = models.TextField()
    contributor = models.CharField(max_length=120)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return (self.text[:60] + '…') if len(self.text) > 60 else self.text


class Picture(models.Model):
    image_url = models.URLField()
    contributor = models.CharField(max_length=120)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Picture by {self.contributor} ({self.image_url})"

