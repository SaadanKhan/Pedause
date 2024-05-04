from django.urls import path
from .views import UserLogin, VerifyOTP, UserLogout, UserSignup, CreateUserProfile, UserSocialLogin


urlpatterns = [
    path('signup/', UserSignup.as_view(), name='signup'),
    path('login/', UserLogin.as_view(), name='login'),
    path('verify_otp/', VerifyOTP.as_view(), name='login'),
    path('logout/', UserLogout.as_view(), name='logout'),
    path('update_profile/', CreateUserProfile.as_view(), name='update_profile'),
    path('social_login/', UserSocialLogin.as_view(), name='social_login'),
]