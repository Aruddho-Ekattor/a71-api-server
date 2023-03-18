from . import views
from django.urls import path

urlpatterns = [
    path('create/', views.UserRegisterView.as_view(), name='create'),
    path('login/', views.UserLoginView.as_view(), name='login'),
]