from django.urls import path
from .views import UserCreateApiView,UserApiView,Social_Auth_Facebook
from rest_framework_simplejwt.views import TokenObtainPairView,TokenRefreshView

urlpatterns = [
    path('',UserApiView.as_view(), name = 'info-page'),
    path('register/',UserCreateApiView.as_view(), name = 'register-page'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register-facebook/', Social_Auth_Facebook.as_view(), name = 'fb-login'),
]