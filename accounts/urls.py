from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.urls import path
from .views import RegisterView, UserProfileView, VerifyEmailView, ResendVerificationEmailView


urlpatterns=[
    path('register/', RegisterView.as_view(), name= 'register'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name= 'token_refresh'),
    path('profile/', UserProfileView.as_view(), name='user_profile'),
    path('verify-email/', VerifyEmailView.as_view(), name='verify_email'),
    path('resend-verification/', ResendVerificationEmailView.as_view(), name='resend_verification'),

]