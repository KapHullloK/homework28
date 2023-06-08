from django.contrib import admin

from ads.models import Ad, Location, Category, User

admin.site.register(Ad)
admin.site.register(Location)
admin.site.register(Category)
admin.site.register(User)
