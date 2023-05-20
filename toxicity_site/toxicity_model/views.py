import os

from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.urls import reverse_lazy
from django.views.generic import CreateView

from .forms import RegisterForm
from .models import SiteUser


# Create your views here.
def home(request, *args, **kwargs):
    return render(request, os.path.join("main", "home.html"))


def user_page(request, *args, **kwargs):
    return render(request, "user_profile.html")


class RegisterUser(CreateView):
    form_class = RegisterForm
    template_name = os.path.join("registration", "sign_up.html")
    success_url = reverse_lazy("user_page")
    #

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        return dict(list(context.items()))

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('home')


class LoginUser(LoginView):
    form_class = AuthenticationForm
    template_name = os.path.join("registration", "login.html")

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        return dict(list(context.items()))

    def get_success_url(self):
        return reverse_lazy("home")


def logout_user(request):
    logout(request)
    return redirect('login')






