from django.urls import path
from account.views import *


urlpatterns = [
    path("send-email-verification-api/", SendEmailVerificationAPIView.as_view(), name="send-email-verification"),
    path("register-view/", RegistrationView.as_view(), name="register-view"),
    path("email-verification-view/", EmailVerificationView.as_view(), name="email-verification-view"),
    path("signup-view/", SignupView.as_view(), name="signup-view"),
    path("login-view/", LoginView.as_view(), name="login-view"),
    path("profile-view/", ProfileView.as_view(), name="profile-view"),
    path("signup-api/", SignupAPIView.as_view(), name="signup-view/"),
    path("login-api/", LoginAPIView.as_view(), name="login-view/"),
    path("logout-api/", LogoutAPIView.as_view(), name="logout-view/"),
    path("get-profile-api/", GetUserProfileAPIView.as_view()),
    path("update-profile-api/", UpdateUserProfileAPIView.as_view(),),
]
