from django.urls import path

from remotenomadsjobs.accounts.views import RegistrationView, LoginView, LogoutView, CompanyDetailstView

urlpatterns = (

    path('registration/', RegistrationView.as_view(), name='registration_user'),
    path('login/', LoginView.as_view(), name='login_user'),
    path('logout/', LogoutView.as_view(), name='logout_user'),
    path('details/<int:pk>', CompanyDetailstView.as_view(), name='company_details'),

)
