from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import views as auth_views, get_user_model

from django.db.models import Count

from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import generic as views

from remotenomadsjobs.accounts.models import RegularUserModel, CompanyUserModel, AppUser
from remotenomadsjobs.jobs.models import JobsModel, JobApplication

from .forms import ContactForm, Deletea
from .models import ContactModel

UserModel = get_user_model()


class UserisVerify(LoginRequiredMixin):
    def dispatch(self, request, *args, **kwargs):
        user = request.user

        if not user.pk:
            return self.handle_no_permission()

        if user.user_type == 'user':
            try:
                RegularUserModel.objects.get(user_id=user.pk)
            except RegularUserModel.DoesNotExist:
                return redirect('save_user')
        elif user.user_type == 'company':
            try:
                CompanyUserModel.objects.get(user_id=user.pk)
            except CompanyUserModel.DoesNotExist:
                return redirect('save_company')
        return super().dispatch(request, *args, **kwargs)


class IndexView(views.DetailView):
    template_name = 'web/index.html'

    def get(self, request, *args, **kwargs):
        advertisements = JobsModel.objects.all()

        for advertisement in advertisements:
            company_user = CompanyUserModel.objects.get(user_id=advertisement.company_id)
            advertisement.company_user = company_user

        return render(request, self.template_name, {'advertisements': advertisements})


class DashboardView(UserisVerify, auth_views.TemplateView):
    template_name = 'web/dashboard.html'

    def get(self, request, *args, **kwargs):
        user = request.user

        if user.user_type == 'user':
            current_user_id = request.user.id
            job_applications = JobApplication.objects.filter(user_id=current_user_id)
            job_ids = job_applications.values_list('job_id', flat=True)
            job_description = JobsModel.objects.filter(id__in=job_ids)

            return render(request, 'web/user_dashboard.html', {'job_description': job_description})

        if user.user_type == 'company':
            current_user_id = request.user.id
            job_applications = JobsModel.objects.filter(company_id=current_user_id).annotate(
                num_applicants=Count('jobapplication'))

            return render(request, 'web/company_dashboard.html', {'jobs': job_applications})

        return render(request, 'web/dashboard.html')


class CompanyProfileCreatView(views.CreateView):
    template_name = 'web/profile_company.html'
    model = CompanyUserModel
    fields = ('company_name', 'company_info', 'company_site', 'company_addres', 'logo',)

    def form_valid(self, form):
        form.instance.user = self.request.user

        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('index')


class UserProfileCreatView(views.CreateView):
    template_name = 'web/profile_user.html'
    model = RegularUserModel
    fields = ('first_name', 'last_name', 'user_motivation', 'user_telephone')

    def form_valid(self, form):
        form.instance.user = self.request.user

        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('index')


class ProfileUpdateView(UserisVerify, views.TemplateView):
    def get(self, request, *args, **kwargs):
        user = request.user

        if user.user_type == 'user':

            return redirect('update_user_profile')
        elif user.user_type == 'company':
            return redirect('update_company_profile')

        return render(request, 'web/dashboard.html')


class UserProfileUpdateView(UserisVerify, views.UpdateView):
    model = RegularUserModel
    template_name = 'web/user_update_profile.html'
    success_url = reverse_lazy('update_profile')

    fields = ('first_name', 'last_name', 'user_motivation', 'user_telephone')

    def get_object(self, queryset=None):
        return RegularUserModel.objects.get(user=self.request.user)

    def form_valid(self, form):
        return super().form_valid(form)


class CompanyProfileUpdateView(UserisVerify, views.UpdateView):
    model = CompanyUserModel
    template_name = 'web/company_update_profile.html'
    success_url = reverse_lazy('update_profile')

    fields = ('company_name', 'company_info', 'company_site', 'company_addres')

    def get_object(self, queryset=None):
        return CompanyUserModel.objects.get(user=self.request.user)

    def form_valid(self, form):
        return super().form_valid(form)


class ContactFormView(views.CreateView):
    model = ContactModel
    form_class = ContactForm
    template_name = 'web/contact_form.html'
    success_url = reverse_lazy('index')


def delete_account(request, pk):
    userd = AppUser.objects.get(pk=pk)
    if request.method == 'POST':
        form = Deletea(request.POST, instance=userd)
        if form.is_valid():
            JobsModel.objects.filter(company_id=pk).delete()
            JobApplication.objects.filter(user_id=pk).delete()
            form.save()
            return redirect('index')
    else:
        form = Deletea(instance=userd)

    context = {'form': form}

    return render(request, 'web/delete_account.html', context)
