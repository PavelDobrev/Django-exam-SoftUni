import kwargs as kwargs
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy, reverse
from django.utils.text import slugify
from django.views import generic as views
from django.shortcuts import render, get_object_or_404, redirect

from remotenomadsjobs.accounts.models import CompanyUserModel
from remotenomadsjobs.jobs.models import JobsModel, JobApplication
from django.contrib.auth import views as auth_views

from remotenomadsjobs.web.views import user_is_verify


# Create your views here.

class user_is_company(LoginRequiredMixin):
    def dispatch(self, request, *args, **kwargs):
        user = request.user
        if not user.user_type == 'company':
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)


class AppView(auth_views.TemplateView):

    def post(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        if request.user.is_authenticated:
            return redirect('user_app', pk=pk)
        else:
            return redirect('login_user')


class UserAppView(views.CreateView):
    template_name = 'jobs/job_app_user.html'
    model = JobApplication
    fields = ('cv', 'user_motivation')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pk = self.kwargs.get('pk')
        context['pk_from_url'] = pk
        return context

    def form_valid(self, form):
        form.instance.user_id = self.request.user.pk
        form.instance.job_id = self.kwargs.get('pk')
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('dashboard')


class CreatJobView(user_is_verify, user_is_company, views.CreateView):
    template_name = 'jobs/new_job.html'
    model = JobsModel
    fields = ('description', 'salary', 'title')

    def form_valid(self, form):
        form.instance.company = self.request.user

        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('index')


class DetailsJobView(views.DetailView):
    template_name = 'jobs/job_details.html'
    model = JobsModel
    fields = ('description', 'salary', 'title')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        job = self.get_object()
        company_user = get_object_or_404(CompanyUserModel, user=job.company)
        context['company_user'] = company_user
        return context


class ViewsCandidateView(LoginRequiredMixin, views.TemplateView):
    template_name = 'jobs/candidate_details.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        job_pk = self.kwargs['pk']
        job = JobsModel.objects.get(pk=job_pk)
        candidates = JobApplication.objects.filter(job_id=job)

        user_id = self.request.user.id

        if user_id != job.company_id:
            return self.handle_no_permission()
        else:
            context['job'] = job
            context['candidates'] = candidates

        return context


class DeleteJobView(views.DeleteView):
    model = JobsModel
    template_name = 'jobs/delete_job.html'
    success_url = reverse_lazy('dashboard')


class DeleteJobAppView(views.DeleteView):
    model = JobApplication
    template_name = 'jobs/delete_job.html'
    success_url = reverse_lazy('dashboard')
