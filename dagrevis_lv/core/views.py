from django.template import RequestContext
from django.shortcuts import render_to_response


def about(request):
    return render_to_response("about.html", context_instance=RequestContext(request))


def contacts(request):
    return render_to_response("contacts.html", context_instance=RequestContext(request))
