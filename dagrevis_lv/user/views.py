from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.forms import UserCreationForm


def registration(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse("user_login"))
    else:
        form = UserCreationForm()
    return render_to_response(
        "registration.html",
        {"form": form},
        context_instance=RequestContext(request)
    )


def logout(request):
    auth_logout(request)
    return HttpResponseRedirect(reverse("blog_articles"))
