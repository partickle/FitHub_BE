from django.contrib import admin
from .models import UserProfile, PremiumSubscription, CustomUser

admin.site.register(CustomUser)
admin.site.register(UserProfile)
admin.site.register(CustomUser)
admin.site.register(PremiumSubscription)
