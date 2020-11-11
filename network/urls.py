
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create", views.createpost, name="create"),
    path("users/<str:username>", views.infouser, name="view_user"),
    path("follow/<str:username>", views.follow, name="follow"),
    path("unfollow/<str:username>", views.unfollow, name="unfollow"),
    path("following", views.following, name="following"),
    path("edit/<int:postid>", views.edit, name="edit"),
    path("like/<int:postid>", views.like, name="like_post"),
]
