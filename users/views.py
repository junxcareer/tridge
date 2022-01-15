from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login

from .forms import LoginForm


class LoginView(generic.FormView):
    template_name = "users/login.html"
    form_class = LoginForm
    success_url = reverse_lazy("polls:index")

    def form_valid(self, form):
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = authenticate(self.request, username=username, password=password)
        if user:
            login(self.request, user)
        return super().form_valid(form)


class SignUpView(generic.edit.CreateView):
    template_name = "users/signup.html"
    form_class = UserCreationForm
    success_url = reverse_lazy("users:login")
