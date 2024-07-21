from django.contrib import admin
from django.urls import path
from . import views

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

app_name = 'my_account'
urlpatterns = [
    path('register/',views.PassengerRegistrationView.as_view(),name="registration"),
    path('register-driver/',views.DriverRegistrationView.as_view(),name="driver-reg"),
    path('login/', views.LoginView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('user/<uuid:pk>',views.UserRetriveUpdateApiView.as_view(),name='retrive_user'),
    path('otp/resent-otp-verification-code/',views.ResendOtpcode.as_view(),name="resent_otp"),
    path('otp/verify/',views.VerifyUserOtp.as_view(),name="verify_otp"),
]