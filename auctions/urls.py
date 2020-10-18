from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("add", views.price, name="add"),
    path("listing/<int:id>", views.info, name="info"),
    path("create", views.create, name="create"),
    path("watchlist", views.watchlist, name="watch"),
    path("addw/<int:listingid>", views.addwatch, name="addw"),
    path("removew/<int:listingid>", views.removewatch, name="removew"),
    path("category/<str:category>", views.category, name="c"),
    path("comment/<int:listing>", views.comments, name="comment"),
    path("bid/<int:listing>", views.subbid, name="bid"),
    path("closebid/<int:listing>", views.closebid, name="close")
]
