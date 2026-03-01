from django.db import models
from django.conf import settings


class Paragraph(models.Model):
    """User paragraph for text analysis."""
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Paragraph {self.id}"


class WordFrequency(models.Model):
    """Word frequency tracking per user."""
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    word = models.CharField(max_length=100)
    count = models.IntegerField(default=0)

    class Meta:
        unique_together = ('user', 'word')

    def __str__(self):
        return f"{self.word} ({self.count})"