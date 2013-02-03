from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse


def legacy_blog_article(request, article_pk):
    return HttpResponseRedirect(reverse("blog_article", kwargs={"article_pk": article_pk}))
