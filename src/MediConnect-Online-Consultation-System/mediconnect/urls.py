"""
URL configuration for mediconnect project.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from dashboard.views import landing

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', landing, name='home'),
    path('accounts/', include('accounts.urls')),
    path('dashboard/', include('dashboard.urls')),
    path('consultations/', include('consultations.urls')),
    path('prescriptions/', include('prescriptions.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    from mediconnect.demo_views import setup_demo_view, login_demo_view
    urlpatterns += [
        path('debug/setup-demo/', setup_demo_view, name='setup_demo'),
        path('debug/login-demo/<str:username>/', login_demo_view, name='login_demo'),
    ]
