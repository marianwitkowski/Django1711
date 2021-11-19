from django.shortcuts import render, get_object_or_404, redirect
from django.http.request import HttpRequest
from django.http.response import HttpResponse, Http404
# Create your views here.
from datetime import datetime

# import modeli
from .models import *
from .forms import MovieForm

def hello_world(request : HttpRequest):
    s = "<h1>Hello world!!!</h1>"
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

def moviedel_response(request, id):
    #_movie = get_object_or_404(Movie, pk=id)
    _movie = None
    try:
        _movie = Movie.objects.get(pk=id)
    except:
        raise Http404("nie ma takiego filmu")

    if request.method == "POST":
        #usunąć obiekt
        _movie.delete()
        return redirect(movielist_response)
    return render(request, "movie-del.html", {
        "movie": _movie
    })

from django.conf import settings

def movieadd_response(request : HttpRequest):
    if not request.user.is_authenticated:
        return redirect(f"/admin?next={request.path}")

    form = MovieForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        movie = form.save(commit=True)
        movie.author = request.user
        movie.save()
        return redirect(movielist_response)
    return render(request, "movie-add.html", { "form" : form })

def movieedit_response(request, id):
    _movie = get_object_or_404(Movie, pk=id)
    form = MovieForm(request.POST or None, request.FILES or None, instance=_movie)
    if form.is_valid():
        form.save(commit=True)
        return redirect(movielist_response)
    return render(request, "movie-add.html", { "form" : form, "edit" : True })