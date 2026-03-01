from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Paragraph, WordFrequency
from .tasks import process_paragraph


@login_required
def dashboard_view(request):
    """Main dashboard for paragraph submission and word frequency display."""
    if request.method == "POST":
        text = request.POST.get("text")

        if text:
            paragraphs = text.split("\n\n")

            for para in paragraphs:
                para = para.strip()
                if para:
                    p = Paragraph.objects.create(
                        user=request.user,
                        content=para
                    )
                    try:
                        process_paragraph.delay(p.id)
                    except Exception:
                        # Fallback to synchronous processing if Celery is not available
                        process_paragraph(p.id)

    words = WordFrequency.objects.filter(user=request.user).order_by('-count')

    return render(request, "dashboard.html", {"words": words})


@login_required
def search_view(request):
    """Search for words across user paragraphs."""
    word = request.GET.get("word")
    results = []

    if word:
        word = word.lower()

        paragraphs = Paragraph.objects.filter(user=request.user)

        paragraph_list = []

        for para in paragraphs:
            words = para.content.lower().split()
            count = words.count(word)

            if count > 0:
                paragraph_list.append({
                    "content": para.content,
                    "count": count
                })

        paragraph_list = sorted(
            paragraph_list,
            key=lambda x: x["count"],
            reverse=True
        )[:10]

        results = paragraph_list

    return render(request, "search.html", {
        "word": word,
        "results": results
    })