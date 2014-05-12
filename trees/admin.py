from django.contrib import admin
from predictions.models import Event, Category, Share, ShareTransaction, UserTransaction, UserProfile

admin.site.register(Event)
admin.site.register(Category)
admin.site.register(Share)
admin.site.register(ShareTransaction)
admin.site.register(UserProfile)
admin.site.register(UserTransaction)