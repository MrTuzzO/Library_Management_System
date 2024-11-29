from django.urls import path
from . import views

urlpatterns = [
    path('deposit/', views.deposit_money, name='deposit_money'),
    path('signup/', views.signup, name='signup'),
    path('profile/', views.profile, name='profile'),
    path('login/', views.UserLogin.as_view(), name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('edit_profile/', views.edit_profile, name='edit_profile'),
    path('change_password/', views.change_password, name='change_password'),
]
