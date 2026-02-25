from django.urls import path
from .views import login_user, register_user, test_user_api

urlpatterns = [
    path('login/', login_user),
    path('register/', register_user),
    path('test/', test_user_api),
]
