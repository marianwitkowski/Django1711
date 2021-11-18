from django.urls import path
from .views import *

urlpatterns = [
    path("hello", hello_world),
    path("req", request_details),
    path("now/", show_now),

    path("movielist", movielist_response, name="movie_list"),
    path("movieinfo/<int:id>/", movieinfo_response, name="movie_info"),
    path("moviedel/<int:id>/", moviedel_response, name="movie_del"),
]