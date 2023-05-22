from django.contrib import admin
from django.urls import path, include

from . import views

su = views.SiteUser()

urlpatterns = [
    path('', su.home, name="home"),
    path('admin/', admin.site.urls, name="admin"),
    path('register/', views.RegisterUser.as_view(), name="register"),
    path('login/', views.LoginUser.as_view(), name="login"),
    path('logout/', views.logout_user, name="logout"),
    path('user_page', su.user_page, name="user_page"),
    path('requests_history', su.get_requests, name="requests_history"),
    path('make_requests', su.user_page, name="make_request"),
]
