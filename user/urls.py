from django.urls import path
from .views import UserCreateApiView,UserApiView

urlpatterns = [
    path('',UserApiView.as_view(), name = 'login-page'),
    path('register/',UserCreateApiView.as_view(), name = 'register-page'),
    # path('register-facebook/',name = 'fb-login'),
]