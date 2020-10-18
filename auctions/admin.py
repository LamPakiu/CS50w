from django.contrib import admin

from .models import createlisting, Watchlist, comment, bid, User
# Register your models here.

admin.site.register(createlisting)
admin.site.register(Watchlist)
admin.site.register(comment)
admin.site.register(bid)
admin.site.register(User)