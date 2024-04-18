from django import forms
from .models import ContactModel
from ..accounts.models import AppUser

class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactModel
        fields = ['email', 'name', 'message'] 

        widgets = {
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Name'}),
            'message': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Message'}),
        }


class Deletea(forms.ModelForm):
    def save(self, commit=True):
        self.instance.delete()
        return self.instance

    class Meta:
        model = AppUser
        fields = ()