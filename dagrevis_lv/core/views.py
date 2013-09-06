import logging

from django.core.mail import send_mail
from django.http import HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response, redirect
from django.utils.translation import ugettext
from django.conf import settings

from core.forms import FreelanceForm


logger = logging.getLogger(__name__)


def about(request):
    return render_to_response("about.html", {"page_title": ugettext("About")},
                              context_instance=RequestContext(request))


def contacts(request):
    return render_to_response("contacts.html",
                              {"page_title": ugettext("Contacts")},
                              context_instance=RequestContext(request))


def robots_txt(request):
    return HttpResponse(settings.CONTENTS_OF_ROBOTS_TXT,
                        content_type="text/plain")


def humans_txt(request):
    return HttpResponse(settings.CONTENTS_OF_HUMANS_TXT,
                        content_type="text/plain")


def freelance(request):
    if not settings.FREELANCE_AVAILABLE:
        return redirect("blog_articles")
    if request.method == "POST":
        freelance_form = FreelanceForm(request.POST)
        if freelance_form.is_valid():
            send_mail("Freelance offer",
                      freelance_form.cleaned_data["message"],
                      freelance_form.cleaned_data["client_email"],
                      [settings.AUTHOR_EMAIL])
            return redirect("blog_articles")
    else:
        freelance_form = FreelanceForm()
    return render_to_response("freelance.html",
                              {
                                  "page_title": ugettext("Freelance"),
                                  "freelance_form": freelance_form,
                              },
                              context_instance=RequestContext(request))
