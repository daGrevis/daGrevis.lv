from django.http import HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.utils.translation import ugettext
from django.conf import settings


def about(request):
    return render_to_response("about.html", {"page_title": ugettext("About")}, context_instance=RequestContext(request))


def contacts(request):
    return render_to_response("contacts.html", {"page_title": ugettext("Contacts")}, context_instance=RequestContext(request))


def robots_txt(request):
    return HttpResponse(settings.CONTENTS_OF_ROBOTS_TXT, content_type="text/plain")


def humans_txt(request):
    return HttpResponse(settings.CONTENTS_OF_HUMANS_TXT, content_type="text/plain")
