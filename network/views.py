import json
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect,  get_object_or_404
from django.urls import reverse
from django.core.paginator import Paginator
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required

from .models import User, post, profile


def index(request):
    allposts = post.objects.all().order_by('id').reverse()
    paginator = Paginator(allposts, 10)
    page_number = request.GET.get('page')
    posts = paginator.get_page(page_number)
    if request.user.is_authenticated:
        liked_posts = request.user.liked_posts.all()
    else:
        liked_posts = []
    return render(request, "network/index.html",{
        "posts" : posts,
        "title": "All Posts",
        'liked_posts': liked_posts
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
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


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
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")

def createpost(request):
    if request.method == 'POST':
        create = post(user= request.user)
        create.owner = request.user
        create.body = request.POST.get('body')
        create.save()

        return redirect('index')

    else:
        return render(request, 'network/index.html')

def infouser(request, username):
    account = User.objects.get(username = username)
    print (account.id)
    identity = account.id
    followers = account.followers.count()
    following = account.followed_accounts.count()
    if account.followers.filter(follower=request.user).exists():
        follower = True
    else:
        follower = False
    allposts = account.user_posts.all().order_by('id').reverse()
    paginator = Paginator(allposts, 10)
    page_number = request.GET.get('page')
    posts = paginator.get_page(page_number)
    if request.user.is_authenticated:
        liked_posts = request.user.liked_posts.all()
    else:
        liked_posts = []
    return render(request, "network/profile.html", {
        "account": account,
        "followers": followers,
        "following": following,
        "follower": follower,
        "posts" : posts,
        "identity" : identity,
        'liked_posts': liked_posts
    })


def follow(request, username):
    account = User.objects.get(username = username)
    print (account.id)
    followea = account.id
    if request.user:
        f = profile(follower=request.user, followee=account)
        f.save()
        return HttpResponseRedirect(reverse("view_user", args=(username,))) 

    else:
        return render(request, 'network/index.html')

def unfollow(request, username):
    account = User.objects.get(username = username)
    print (account.id)
    followea = account.id
    if request.user:
        f = profile.objects.get(follower=request.user, followee=account)
        f.delete()
        return HttpResponseRedirect(reverse("view_user", args=(username,))) 

    else:
        return render(request, 'network/index.html')

def following(request):
        account = request.user
        following = account.followed_accounts.all()
        followedaccounts = []
        for account in following:
            followedaccounts.append(account.followee)
        allposts =  post.objects.filter(user__in=followedaccounts).order_by('id').reverse()
        paginator = Paginator(allposts, 10)
        page_number = request.GET.get('page')
        posts = paginator.get_page(page_number)
        title = "Posts by accounts followed by " + request.user.username
        if request.user.is_authenticated:
            liked_posts = request.user.liked_posts.all()
        else:
            liked_posts = []
        return render(request, "network/index.html", {
            'posts': posts,
            'title': title,
            'followedaccounts': followedaccounts,
            'liked_posts': liked_posts
        })
        
@csrf_exempt
@login_required
def edit(request, postid):
    try:
        bpost = post.objects.get(id=postid)
    except bpost.DoesNotExist:
        return JsonResponse({"error": "post not found."}, status=404)
    if request.method == "GET":
        return JsonResponse(bpost.serialize())
    elif request.method == "PUT":
        data = json.loads(request.body)
        if bpost.user == request.user :
            if data.get("body") is not None:
                bpost.body = data["body"]
        else:
            return JsonResponse({"error":"INVALID ACCESS"},status=404)
        bpost.save()
        return HttpResponse(status=204)
    else:
        return JsonResponse({"error": "try using GET request"}, status=404)

@login_required
def like(request, postid):
    itempost = post.objects.get(pk=postid)
    user = request.user

    if user in itempost.likes.all():
        itempost.likes.remove(user)
    else:
        itempost.likes.add(user)

    return JsonResponse({"message" : "success"})
