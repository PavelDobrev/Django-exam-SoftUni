from django import forms
from django.contrib.auth import forms as auth_forms, get_user_model, authenticate
from django.contrib.auth.forms import AuthenticationForm

from django.core.exceptions import ValidationError

from remotenomadsjobs.accounts.models import AppUser

UserModel = get_user_model()


class UserLoginForm(AuthenticationForm):
    username = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}), label="Email")
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if not UserModel.objects.filter(email=username).exists():
            raise ValidationError("There is no user registered with the specified email address.")
        return username

    def clean(self):
        super().clean() 
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if username and password:
            user = authenticate(email=username, password=password)
            if user is None:
                raise ValidationError("The password is incorrect.")
        
        return self.cleaned_data


class RegisterUserForm(auth_forms.UserCreationForm):
    user_type = forms.ChoiceField(
        choices=UserModel.USER_TYPE_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'}),

    )

    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    class Meta(auth_forms.UserCreationForm.Meta):
        model = UserModel
        fields = ('email', 'user_type', 'password1', 'password2',)

    def clean_email(self):
        email = self.cleaned_data['email']
        if AppUser.objects.filter(email=email).exists():
            raise ValidationError("Email already registered.")
        return email

    def clean(self):
        super().clean() 
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise ValidationError("Passwords do not match.")
        return self.cleaned_data