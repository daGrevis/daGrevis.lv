from django.template import RequestContext
from django.shortcuts import render_to_response
from django.utils.translation import ugettext


def about(request):
    return render_to_response("about.html", {"page_title": ugettext("About")}, context_instance=RequestContext(request))


def contacts(request):
    return render_to_response("contacts.html", {"page_title": ugettext("Contacts")}, context_instance=RequestContext(request))
