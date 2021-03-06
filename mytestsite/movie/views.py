from django.shortcuts import render, get_object_or_404, redirect
from django.http.request import HttpRequest
from django.http.response import HttpResponse, Http404
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.utils.translation import ugettext as _

# Create your views here.
from datetime import datetime

# import modeli
from .models import *
# import formularzy
from .forms import MovieForm, SignupForm

from django.utils import translation

def changelang_response(request: HttpRequest):
    user_lng = request.GET.get("l")
    translation.activate(user_lng)
    response = HttpResponse("OK")
    response.set_cookie(settings.LANGUAGE_COOKIE_NAME, user_lng)
    return redirect("/hello")

def hello_world(request : HttpRequest):
    txt = _('WelcomeHeading')
    s = f"<h1>{txt}</h1>"
    return HttpResponse(s)

def request_details(request: HttpRequest):
    #print("request_details")
    param_a = request.GET.get("a",-1)
    param_b = request.GET.get("b","---")
    s = f"Param A:{param_a}, Param B:{param_b}<br/>Path: {request.path}"

    headers = [str(item) for item in request.headers.items()]
    headers_str = "<br/>".join(headers)
    return HttpResponse(f"{s}<br/>{headers_str}")

def show_now(request: HttpRequest):
    ctx = {
        "current_ts" : datetime.now(),
        "hour" : 19, # datetime.now().hour
        "items": [], #["Ala","ma","kota"],
        "total_item": 3
    }
    return render(request, "test.html", ctx )

def movielist_response(request):
    all_movies = Movie.objects.all().order_by("title")
    return render(request, "movie-list.html", {
        "movies" : all_movies
    })

def movieinfo_response(request, id):
    _movie = get_object_or_404(Movie, pk=id)
    _comments = Comment.objects.filter(movie=_movie)
    return render(request, "movie-info.html", {
        "movie" : _movie, "comments" : _comments
    })

@login_required()
def moviedel_response(request, id):
    #_movie = get_object_or_404(Movie, pk=id)
    _movie = None
    try:
        _movie = Movie.objects.get(pk=id)
    except:
        raise Http404("nie ma takiego filmu")

    if request.method == "POST":
        #usun???? obiekt
        _movie.delete()
        return redirect(movielist_response)
    return render(request, "movie-del.html", {
        "movie": _movie
    })


@login_required()
def movieadd_response(request : HttpRequest):
    # if not request.user.is_authenticated:
    #     return redirect(f"/admin/login?next=/movieadd/")

    form = MovieForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        movie = form.save(commit=True)
        movie.author = request.user
        movie.save()
        return redirect(movielist_response)
    return render(request, "movie-add.html", { "form" : form })

@login_required()
def movieedit_response(request, id):
    _movie = get_object_or_404(Movie, pk=id)
    form = MovieForm(request.POST or None, request.FILES or None, instance=_movie)
    if form.is_valid():
        form.save(commit=True)
        return redirect(movielist_response)
    return render(request, "movie-add.html", { "form" : form, "edit" : True })

def logout_done(request):
    return render(request, "logout-done.html")

import hashlib
def signup_reponse(request):
    if request.method == "POST":
        form = SignupForm(request.POST)
        result = form.is_valid()
        if result:
            cu = CustomUser()
            cu.first_name = form["first_name"].value()
            cu.last_name = form["last_name"].value()
            cu.email = form["email"].value()
            cu.age = form["age"].value()
            s = hashlib.md5(form["password1"].value().encode("utf-8")). hexdigest()
            cu.password = s
            cu.save()
    else:
        form = SignupForm()
    return render(request, "signup.html", {"form":form})

def form_response(request : HttpRequest):
    if request.method == "POST":
        #obs??uga formularza
        fn = request.POST.get("fullname")
        age = request.POST.get("age")
        # walidacja danych z formularza
        if age < 0:
            pass
        # zapis
    return render(request, "form.html")

from .tasks import task_send_email, long_task
def celerytest_response(request):
    token = long_task.delay()
    return HttpResponse(token)


import json
from celery.result import AsyncResult
def gettask_response(request, token):
    result = AsyncResult(token)
    response_data = {
        "state" : result.state,
        "details": result.info
    }
    return HttpResponse(json.dumps(response_data), content_type="application/json")