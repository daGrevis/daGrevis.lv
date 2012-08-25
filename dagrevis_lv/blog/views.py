from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404
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


def article(request, article_pk, slug):
    article = get_object_or_404(Article, pk=article_pk)
    return render_to_response(
        "article.html",
        {
            "article": article,
        },
        context_instance=RequestContext(request),
    )
