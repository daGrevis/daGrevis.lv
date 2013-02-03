from django import http
from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.conf import settings
from django.utils.translation import ugettext
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from blog.models import Article, Comment, Tag
from blog.forms import CommentForm
from blog.forms import SearchForm


def articles(request):
    articles = Article.objects.order_by("-pk")
    paginator = Paginator(articles, settings.ARTICLE_COUNT_PER_PAGE)
    page = request.GET.get("page")
    try:
        articles = paginator.page(page)
    except PageNotAnInteger:
        articles = paginator.page(1)
    except EmptyPage:
        articles = paginator.page(paginator.num_pages)
    sorted_articles = Article.sort_articles_by_month(articles)
    return render_to_response(
        "articles.html",
        {
            "page_title": ugettext("Blog"),
            "articles": articles,
            "sorted_articles": sorted_articles,
        },
        context_instance=RequestContext(request)
    )


#TODO: Refactor. Too much code here...
def article(request, article_pk, slug=None):
    article = get_object_or_404(Article, pk=article_pk)
    # If slug is incorrect, "redirect friendly" to URL with correct slug.
    if not slug or slug != article.slug:
        return http.HttpResponsePermanentRedirect(article.get_absolute_url())
    if request.method == "POST":
        # Comment adding.
        if request.user.is_anonymous():
            return http.HttpResponseForbidden()
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.article = article
            comment.author = request.user
            comment_pk_to_reply = request.POST.get("comment_pk_to_reply")
            if comment_pk_to_reply:
                parent = get_object_or_404(Comment, pk=comment_pk_to_reply)
                if parent == comment:
                    return http.HttpResponseForbidden("Comment can't be child for itself.")
                if parent.get_depth() >= settings.MAXIMUM_DEPTH_FOR_COMMENT:
                    return http.HttpResponseForbidden("Comments can't go deeper than {} levels.".format(settings.MAXIMUM_DEPTH_FOR_COMMENT))
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
    tags = article.tag_set.all()
    return render_to_response(
        "article.html",
        {
            "page_title": article.title,
            "article": article,
            "comments": comments,
            "tags": tags,
            "comment_form": comment_form,
            "comment_pk_to_reply": request.GET.get("comment_pk_to_reply"),
        },
        context_instance=RequestContext(request),
    )


def tags(request):
    tags = Tag.get_tags_by_priority()
    return render_to_response(
        "tags.html",
        {
            "page_title": ugettext("Tags"),
            "tags": tags,
        },
        context_instance=RequestContext(request),
    )


def search(request):
    search_form = SearchForm(request.GET)
    found_articles = []
    if search_form.is_valid():
        found_articles = Article.search_articles(search_form.cleaned_data["phrase"], search_form.cleaned_data["tags"])
    return render_to_response(
        "search.html",
        {
            "page_title": ugettext("Search"),
            "found_articles": found_articles,
            "search_form": search_form,
        },
        context_instance=RequestContext(request),
    )
