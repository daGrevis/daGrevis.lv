from django.http import HttpResponsePermanentRedirect
from django.core.urlresolvers import reverse
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


def article(request, article_pk, slug=None):
    article = get_object_or_404(Article, pk=article_pk)
    # If slug is incorrect, "redirect friendly" to URL with correct slug.
    if not slug or slug != article.slug:
        return HttpResponsePermanentRedirect(
            reverse("blog_article", kwargs={"article_pk": article_pk, "slug": article.slug})
        )
    return render_to_response(
        "article.html",
        {
            "article": article,
        },
        context_instance=RequestContext(request),
    )
