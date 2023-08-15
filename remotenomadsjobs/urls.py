
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('remotenomadsjobs.web.urls')),
    path('account/', include('remotenomadsjobs.accounts.urls')),
    path('jobs/', include('remotenomadsjobs.jobs.urls'))
]
