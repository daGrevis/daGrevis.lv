from django import http
from django.core.urlresolvers import reverse
from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404, redirect

from blog.models import Article, Comment, CommentForm


def articles(request):
    articles = Article.objects.order_by("-id")
    return render_to_response("articles.html", {"articles": articles}, context_instance=RequestContext(request))


#TODO: Refactor. Too much code here...
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
            parent_pk = request.POST.get("parent_pk")
            if parent_pk:
                parent = get_object_or_404(Comment, pk=parent_pk)
                if parent == comment:
                    return http.HttpResponseForbidden("Comment can't be child for itself!")
                comment.parent = parent
            comment.save()
            return redirect(
                "blog_article",
                article_pk=article.pk,
                slug=article.slug,
            )
    else:
        comment_form = CommentForm()
    comments = article.comment_set.all()
    comments = Comment.calculate_depth_and_sort(comments)
    return render_to_response(
        "article.html",
        {
            "article": article,
            "comments": comments,
            "comment_form": comment_form,
            "parent_pk": request.GET.get("parent_pk"),
        },
        context_instance=RequestContext(request),
    )
