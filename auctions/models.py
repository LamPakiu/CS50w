from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class createlisting(models.Model):
    title = models.CharField(max_length=64 , null=True)
    images = models.URLField(max_length=200,default=None,blank=True,null=True)
    contents = models.CharField(max_length=500 , null=True)
    price = models.IntegerField(null=True)
    category = models.CharField(max_length=64, null=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.id}: {self.title} "

class Watchlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="watchlists")
    listingid = models.ForeignKey(createlisting, on_delete=models.CASCADE, related_name="createlisting")

    def __str__(self):
        return f"{self.listingid} {self.user}"  

class comment(models.Model):
    comment = models.CharField(max_length=200, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    listing = models.ForeignKey(createlisting, on_delete=models.CASCADE, related_name="create")

    def __str__(self):
        return f"{self.comment}"

class bid(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bid")
    bid = models.IntegerField()
    listing = models.ForeignKey(createlisting, on_delete=models.CASCADE, related_name="listing")

    def __str__(self):
        return f"{self.user} {self.bid} {self.listing}"

class closebid(models.Model):
    user = models.ForeignKey(User,  on_delete=models.CASCADE )
    win = models.ForeignKey(createlisting, on_delete=models.CASCADE, related_name="win")
    listing = models.ForeignKey(createlisting, on_delete=models.CASCADE, related_name="item")

    def __str__(self):
        return f"{self.user} {self.win} {self.listing}"