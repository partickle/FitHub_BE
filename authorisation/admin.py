from django.contrib import admin
from .models import UserProfile, PremiumSubscription

admin.site.register(UserProfile)
admin.site.register(PremiumSubscription)
