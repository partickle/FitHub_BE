from django.urls import path
from authorisation.views import DeleteAccountView, UserProfileUpdateView

urlpatterns = [
    path('update/', UserProfileUpdateView.as_view(), name='profile-update'),
    path('delete/', DeleteAccountView.as_view(), name='delete-account'),

]
