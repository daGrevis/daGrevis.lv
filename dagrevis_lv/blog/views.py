import logging

from django import http
from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.conf import settings
from django.utils.translation import ugettext
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from blog.models import Article, Tag
from blog.forms import CommentForm
from blog.forms import SearchForm


logger = logging.getLogger(__name__)


def articles(request):
    articles = Article.objects.filter(is_draft=False).order_by("-pk")
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


def article(request, article_pk, slug=None):
    article = get_object_or_404(Article, pk=article_pk, is_draft=False)
    # If slug is incorrect, "redirect friendly" to the correct link.
    if not slug or slug != article.slug:
        return http.HttpResponsePermanentRedirect(article.get_absolute_url())
    if request.method == "POST":
        user = request.user
        if user.is_anonymous():
            return http.HttpResponseForbidden()
        comment_form = CommentForm(request.POST, user=user)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.author = user
            comment.save()
            link = "{}{}".format(article.get_absolute_url(),
                                 "#comment{}".format(comment.pk))
            return redirect(link)
    else:
        comment_form = CommentForm()
    return render_to_response(
        "article.html",
        {
            "page_title": article.title,
            "article": article,
            "comment_form": comment_form,
            "comment_pk": request.GET.get("comment_pk"),
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
        found_articles = (Article.search_articles(
                          search_form.cleaned_data["phrase"],
                          search_form.cleaned_data["tags"]))
    return render_to_response(
        "search.html",
        {
            "page_title": ugettext("Search"),
            "found_articles": found_articles,
            "search_form": search_form,
        },
        context_instance=RequestContext(request),
    )
