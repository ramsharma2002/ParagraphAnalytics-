from celery import shared_task
from .models import Paragraph, WordFrequency


@shared_task
def process_paragraph(paragraph_id):
    """Process paragraph and update word frequencies."""
    paragraph = Paragraph.objects.get(id=paragraph_id)
    words = paragraph.content.split()

    for word in words:
        word = word.lower()

        obj, created = WordFrequency.objects.get_or_create(
            user=paragraph.user,
            word=word
        )

        obj.count += 1
        obj.save()