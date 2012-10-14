from django import http
from django.core.urlresolvers import reverse
from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404, redirect

from blog.models import Article, CommentForm


def articles(request):
    articles = Article.objects.order_by("-id")
    return render_to_response("articles.html", {"articles": articles}, context_instance=RequestContext(request))


def article(request, article_pk, slug=None):
    article = get_object_or_404(Article, pk=article_pk)
    # If slug is incorrect, "redirect friendly" to URL with correct slug.
    if not slug or slug != article.slug:
        return http.HttpResponsePermanentRedirect(reverse(
            "blog_article", kwargs={
                "article_pk": article_pk,
                "slug": article.slug,
            },
        ))
    if request.method == "POST":
        # Comment adding.
        if request.user.is_anonymous():
            return http.HttpResponseForbidden()
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.article = article
            comment.author = request.user
            comment.save()
            return redirect(
                "blog_article",
                article_pk=article.pk,
                slug=article.slug,
            )
    else:
        comment_form = CommentForm()
    comments = article.comment_set.all()
    return render_to_response(
        "article.html",
        {
            "article": article,
            "comments": comments,
            "comment_form": comment_form,
        },
        context_instance=RequestContext(request),
    )
