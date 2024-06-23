from django.contrib import admin
from .models import PremiumSubscription, CustomUser

admin.site.register(CustomUser)
admin.site.register(PremiumSubscription)
