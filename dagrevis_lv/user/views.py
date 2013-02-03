from django.http import HttpResponseRedirect, HttpResponseForbidden
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.utils.translation import ugettext
from django.contrib.auth.forms import AuthenticationForm
from django.utils.http import is_safe_url

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
        {
            "page_title": ugettext("Registration"),
            "form": form,
        },
        context_instance=RequestContext(request)
    )


def login(request):
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            auth_login(request, form.get_user())
            redirect_to = request.REQUEST.get("redirect_to")
            if is_safe_url(url=redirect_to, host=request.get_host()):
                return HttpResponseRedirect(redirect_to)
            return HttpResponseRedirect(reverse("blog_articles"))
    else:
        form = AuthenticationForm(request)
    return render_to_response(
        "login.html",
        {
            "page_title": ugettext("Login"),
            "form": form,
        },
        context_instance=RequestContext(request)
    )


def logout(request):
    auth_logout(request)
    return HttpResponseRedirect(reverse("blog_articles"))
