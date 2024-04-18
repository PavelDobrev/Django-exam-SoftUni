from django.contrib import admin

from remotenomadsjobs.accounts.models import CompanyUserModel, AppUser
from remotenomadsjobs.jobs.models import JobsModel
from remotenomadsjobs.web.models import ContactModel


@admin.register(ContactModel)
class ContactModelAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'message')

    def has_view_permission(self, request, obj=None):
        return request.user.is_superuser


class JobsModelAdmin(admin.ModelAdmin):
    list_display = ('title', 'description')


class CompanyUserAdmin(admin.ModelAdmin):
    list_display = ('company_name',)


class UserAdmin(admin.ModelAdmin):
    list_display = ('email',)


admin.site.register(AppUser, UserAdmin)
admin.site.register(JobsModel, JobsModelAdmin)
admin.site.register(CompanyUserModel, CompanyUserAdmin)
