from django.urls import reverse_lazy
from django.views import generic as views
from django.contrib.auth import views as auth_views, login

from remotenomadsjobs.accounts.forms import RegisterUserForm, UserLoginForm
from remotenomadsjobs.accounts.models import CompanyUserModel


class CompanyDetailstView(views.DetailView):
    template_name = 'accounts/company_details.html'
    model = CompanyUserModel
    fields = ('company_name', 'company_info', 'company_site', 'company_addres')


class RegistrationView(views.CreateView):
    template_name = 'accounts/registration.html'
    form_class = RegisterUserForm

    def form_valid(self, form):
        result = super().form_valid(form)

        login(self.request, self.object)

        return result

    def get_success_url(self):
        return reverse_lazy('dashboard')


class LoginView(auth_views.LoginView):
    template_name = 'accounts/login.html'
    form_class = UserLoginForm

    def get_success_url(self):
        return reverse_lazy('dashboard')


class LogoutView(auth_views.LogoutView):
    def get_success_url(self):
        return reverse_lazy('index')
