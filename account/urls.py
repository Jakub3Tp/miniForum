from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    #path('login/', views.user_login, name='login')
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('', views.dashboard, name='dashboard'),
    path('register/', views.register, name='register'),
    path('edit/', views.edit, name='edit'),
    path('consoles/', views.console_list, name='console_list'),
    path('consoles/add/', views.add_console, name='add_console'),
    path('consoles/<int:pk>/edit/', views.edit_console, name='edit_console'),
    path('consoles/<int:pk>/', views.console_detail, name='console_detail'),
    path('consoles/<int:pk>/delete/', views.delete_console, name='delete_console'),
]
