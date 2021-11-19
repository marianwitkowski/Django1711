from django.urls import path
from .views import *
from django.contrib.auth import views as auth_views

urlpatterns = [
    path("hello", hello_world),
    path("req", request_details),
    path("now/", show_now),

    path("", movielist_response, name="main_page"),
    path("movielist", movielist_response, name="movie_list"),
    path("movieinfo/<int:id>/", movieinfo_response, name="movie_info"),
    path("moviedel/<int:id>/", moviedel_response, name="movie_del"),
    path("movieedit/<int:id>/", movieedit_response, name="movie_edit"),
    path("movieadd", movieadd_response, name="movie_add"),

    path("login/", auth_views.LoginView.as_view(), name="login"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("logout-done", logout_done),

    path("signup", signup_reponse),
    path("form", form_response)
]