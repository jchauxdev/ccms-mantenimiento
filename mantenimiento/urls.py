from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # Usamos las vistas de login/logout que Django ya trae listas
    path('login/', auth_views.LoginView.as_view(template_name='mantenimiento/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    
    # Nuestro Dashboard
    path('', views.dashboard, name='dashboard'),
]