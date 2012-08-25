from django.template import RequestContext
from django.shortcuts import render_to_response
from blog.models import Article


def articles(request):
    articles = Article.objects.order_by("-id")
    return render_to_response(
        "articles.html",
        {
            "articles": articles,
        },
        context_instance=RequestContext(request),
    )
