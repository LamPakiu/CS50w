from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django import forms
import string
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Max

from .models import User, createlisting, Watchlist, comment, bid



def index(request):
    return render(request, "auctions/index.html",{
        "listings" : createlisting.objects.filter(status=True)
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")

def price(request):
    return render(request, "auctions/add.html")

def info(request, id):
    storage = messages.get_messages(request)
    storage = False
    info = createlisting.objects.get(id=id)
    comments = comment.objects.filter(listing=id)
    bids = bid.objects.filter(listing=id).order_by('-bid').first()
    watchlist = True
    if request.user.is_authenticated:
        if request.user.watchlists.filter(listingid=id):
           watchlist = False
    return render(request, "auctions/info.html", {
        "info": info,
        "watchlist": watchlist,
        "comments" : comments,
        "bids" : bids,
        "storage" : storage,
    })

def create(request):
    if request.method == "POST":
        create = createlisting()
        create.owner = request.user
        create.title = request.POST.get('title')
        print(create.title)
        create.contents = request.POST.get('contents')
        print(create.contents)
        create.price = request.POST.get('price')
        print(create.price)
        create.category = request.POST.get('category')
        print(create.category)
        create.images = request.POST.get('images')
        print(create.images)
        create.status = True
        create.save()
        info = create.id

        return HttpResponseRedirect(reverse("info",kwargs={'id':info})) 
    else:
        return render(request, "auctions/index.html")

@login_required(login_url='login')
def watchlist(request):
    watch = request.user.watchlists.all()
    return render(request, "auctions/watchlist.html", {
        "listings" : watch 
    })

def addwatch(request, listingid):
    if request.user:
        w = Watchlist()
        w.user = request.user
        w.listingid = createlisting.objects.get(id=listingid)
        w.save()
        return HttpResponseRedirect(reverse("info", args=(listingid,))) 
    else:
        return render(request, "auctions/index.html")

def removewatch(request, listingid):
    if request.user:
        w = Watchlist.objects.get(user=request.user,listingid = createlisting.objects.get(id=listingid))
        w.delete()
        return HttpResponseRedirect(reverse("info", args=(listingid,)))  
    else:
        return render(request, "auctions/index.html")

def category(request, category):
    cat = createlisting.objects.filter(category=category, status=True)
    return render(request, "auctions/index.html", {"listings":cat})

def comments(request, listing):
    if request.method == "POST":
        c = comment()
        c.comment = request.POST.get('comment')
        c.user = request.user
        c.listing = createlisting.objects.get(id=listing)
        c.save()
        return HttpResponseRedirect(reverse("info", args=(listing,)))
    else:
        return render(request, "auctions/index.html")

def subbid(request, listing):
    bet = ''
    currentbid = createlisting.objects.get(id=listing)
    currentbid = currentbid.price
    if request.method == "POST" :
        userbid = int(request.POST.get('bid'))
        if userbid > currentbid:
            listingi = createlisting.objects.get(id=listing)
            listingi.price = userbid
            listingi.user = request.user
            listingi.save()
            try:
                if bid.objects.filter(id=listing):
                 bidrow = bid.objects.filter(id=listing)
                 bidrow.delete()
                bet = bid()
                bet.user = request.user
                bet.listing = listingi
                bet.bid = userbid
                bet.save()

            except:
                bet = bid()
                bet.user = request.user
                bet.listing = listingi
                bet.bid = userbid
                bet.save()
            messages.success(request, "Bidding success!!", extra_tags="success")
            return HttpResponseRedirect(reverse("info", args=(listing,)))
        else:
            messages.error(request, "Error: Bidding cannot be the same price or smaller than the current bid!", extra_tags="error")
            return HttpResponseRedirect(reverse("info", args=(listing,)))
    
    else:
        return render(request, "auctions/index.html")
        
def closebid (request, listing):
    if request.method == "POST":
        list = createlisting.objects.get(id=listing)
        list.status = False
        list.save()

        return HttpResponseRedirect(reverse("info", args=(listing,)))
    else:
        return render(request, "auctions/index.html")