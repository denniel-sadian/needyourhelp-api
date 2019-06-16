from django.urls import path, include
from . import views

urlpatterns = [
    path('auth/register/', views.CreateUserView.as_view(), name='register'),
    path('auth/login/', views.LoginView.as_view(), name='login'),
    path('auth/logout/', views.log_out, name='logout'),
    path('auth/me/', views.MeView.as_view(), name='me'),
    path('auth/change-password/', views.ChangePasswordView.as_view(),
         name='change_password')
]
