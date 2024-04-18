from django import forms
from django.core.exceptions import ValidationError
from .models import JobsModel


class JobForm(forms.ModelForm):
    class Meta:
        model = JobsModel
        fields = ('description', 'salary', 'title')

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(JobForm, self).__init__(*args, **kwargs)

    def clean_salary(self):
        salary = self.cleaned_data.get('salary')
        if salary < 0:
            raise ValidationError("Salary cannot be negative.")
        return salary

    def save(self, commit=True):
        job = super().save(commit=False)
        job.company = self.user
        if commit:
            job.save()
        return job