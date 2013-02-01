from django.http import HttpResponseRedirect, HttpResponseForbidden
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response
from django.contrib.auth import logout as auth_logout

from user.forms import CustomUserCreationForm


def registration(request):
    if request.method == "POST":
        if request.POST.get("im_bot") == "on":
            return HttpResponseForbidden("Seems that you are a bot.")
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse("user_login"))
    else:
        form = CustomUserCreationForm()
    return render_to_response(
        "registration.html",
        {"form": form},
        context_instance=RequestContext(request)
    )


def logout(request):
    auth_logout(request)
    return HttpResponseRedirect(reverse("blog_articles"))
