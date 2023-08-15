from django import forms
from django.contrib.auth import forms as auth_forms, get_user_model


UserModel = get_user_model()


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


