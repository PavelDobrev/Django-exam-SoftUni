from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone

from remotenomadsjobs.accounts.models import CompanyUserModel

# Create your models here.
UserModel = get_user_model()


class JobsModel(models.Model):
    company = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    description = models.TextField(max_length=600)
    salary = models.IntegerField()
    creation_date = models.DateTimeField(default=timezone.now, editable=False)
    title = models.CharField(max_length=200)


class JobApplication(models.Model):
    job = models.ForeignKey(JobsModel, on_delete=models.CASCADE)
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    cv = models.FileField(upload_to='cv/')
    user_motivation = models.TextField(max_length=600)
    creation_date = models.DateTimeField(default=timezone.now, editable=False)
