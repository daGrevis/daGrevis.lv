import logging

from django.core.mail import send_mail
from django.http import HttpResponse, HttpResponseForbidden
from django.template import RequestContext
from django.shortcuts import render_to_response, redirect
from django.utils.translation import ugettext
from django.conf import settings

from captcha.widgets import ReCaptcha

from core.forms import ContactForm


logger = logging.getLogger(__name__)


def about(request):
    return render_to_response("about.html", {"page_title": ugettext("About")},
                              context_instance=RequestContext(request))


def contacts(request):
    if request.method == "POST":
        if request.POST.get("im_bot") == "on":
            return HttpResponseForbidden("Seems that you are a bot.")

        data = (request.POST).copy()

        if settings.RECAPTCHA_TESTING:
            data["recaptcha_response_field"] = "PASSED"

        contact_form = ContactForm(data)

        if contact_form.is_valid():
            send_mail(ugettext("Email via {}").format(settings.SITE_TITLE),
                      data["message"], data["email"], [settings.AUTHOR_EMAIL])
            return redirect("blog_articles")
    else:
        contact_form = ContactForm()

    captcha = ReCaptcha(attrs={"theme": "clean"}).render(None, None)

    return render_to_response("contacts.html",
                              {
                                  "page_title": ugettext("Contacts"),
                                  "contact_form": contact_form,
                                  "captcha": captcha,
                              },
                              context_instance=RequestContext(request))


def robots_txt(request):
    return HttpResponse(settings.CONTENTS_OF_ROBOTS_TXT,
                        content_type="text/plain")


def humans_txt(request):
    return HttpResponse(settings.CONTENTS_OF_HUMANS_TXT,
                        content_type="text/plain")


def freelance(request):
    return redirect("core_contacts")
