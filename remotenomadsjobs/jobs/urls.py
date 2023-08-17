from django.urls import path

from remotenomadsjobs.jobs.views import CreatJobView, DetailsJobView, AppView, UserAppView, ViewsCandidateView, \
    DeleteJobView, DeleteJobAppView

urlpatterns = [
    path('new/', CreatJobView.as_view(), name='creat_job'),
    path('<int:pk>', DetailsJobView.as_view(), name='details_job'),

    path('app/<int:pk>', AppView.as_view(), name='app'),
    path('app_user/<int:pk>', UserAppView.as_view(), name='user_app'),

    path('views/<int:pk>', ViewsCandidateView.as_view(), name='views_candidate'),
    path('delete/<int:pk>', DeleteJobView.as_view(), name='delete_job'),
    path('delete_job_app/<int:pk>', DeleteJobAppView.as_view(), name='delete_job_app'),


]
