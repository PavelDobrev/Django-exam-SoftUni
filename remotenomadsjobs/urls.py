
from django.contrib import admin
from django.urls import path, include


from django.conf import settings
from django.conf.urls.static import static



urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('remotenomadsjobs.web.urls')),
    path('account/', include('remotenomadsjobs.accounts.urls')),
    path('jobs/', include('remotenomadsjobs.jobs.urls'))
]



if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)