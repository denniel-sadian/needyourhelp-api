from django.urls import path, include
from . import views

urlpatterns = [
    path('auth/register/', views.CreateUserView.as_view(), name='register'),
    path('auth/login/', views.LoginView.as_view(), name='login'),
    path('auth/logout/', views.log_out, name='logout'),
    path('auth/me/', views.me, name='me')
]
