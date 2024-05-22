from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from authorisation.views import SendActivationCodeView, VerifyActivationCodeView


urlpatterns = [
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('send-activation/', SendActivationCodeView.as_view(), name='send-activation-code'),
    path('verify/', VerifyActivationCodeView.as_view(), name='verify-activation-code'),
    # path('register/', RegisterAPIView.as_view(), name='register'),
    # path('login/', LoginAPIView.as_view(), name='login'),

]
