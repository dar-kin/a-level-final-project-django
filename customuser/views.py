from django.views.generic import CreateView, TemplateView
from django.contrib.auth.views import LoginView, LogoutView
from .forms import MyUserCreationForm
from django.urls import reverse_lazy


class Login(LoginView):
    redirect_authenticated_user = True
    template_name = "login.html"


class Logout(LogoutView):
    template_name = "logged_out.html"


class Register(CreateView):
    form_class = MyUserCreationForm
    template_name = "register.html"
    success_url = reverse_lazy("customuser:login")


class MainView(TemplateView):
    template_name = "main.html"