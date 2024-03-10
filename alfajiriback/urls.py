from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include, re_path
from django.views.static import serve

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include(('accounts.urls', 'accounts'), namespace='accounts')),
    path('jobs/', include(('jobs.urls', 'jobs'), namespace='jobs')),
    path('companies/', include(('companies.urls', 'companies'), namespace='companies')),
    path('locations/', include(('locations.urls', 'locations'), namespace='locations')),
    path('categories/', include(('categories.urls', 'categories'), namespace='categories')),
    path('payments/', include(('payments.urls', 'payments'), namespace='payments')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) \
+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
