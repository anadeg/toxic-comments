from django.contrib import admin
from django.urls import path, include

from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('admin/', admin.site.urls, name="admin"),
    path('register/', views.RegisterUser.as_view(), name="register"),
    path('login/', views.LoginUser.as_view(), name="login"),
    path('logout/', views.logout_user, name="logout"),
    path('user_page', views.user_page, name="user_page"),
    path('requests_history', views.home, name="requests_history"),
    path('make_requests', views.home, name="make_request"),
]
