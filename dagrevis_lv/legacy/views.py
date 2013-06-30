import logging

from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse


logger = logging.getLogger(__name__)


def legacy_blog_article(request, article_pk):
    return HttpResponseRedirect(reverse("blog_article",
                                kwargs={"article_pk": article_pk}))


def legacy_blog_articles(request):
    return HttpResponseRedirect(reverse("blog_articles"))
