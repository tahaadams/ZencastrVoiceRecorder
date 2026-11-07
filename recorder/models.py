from django.db import models

class Recording(models.Model):
    title = models.CharField(max_length=100)
    audio_file = models.FileField(upload_to='recordings/')
    transcript = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']


    def __str__(self):
        return f"Recording {self.title} ({self.created_at:%Y-%m-%d %H:%M:%S})"