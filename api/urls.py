from django.urls import path
from .views import *

urlpatterns = [
    path('api-auth/<str:method_name>/', AuthAPI.as_view(), name='auth'),
]