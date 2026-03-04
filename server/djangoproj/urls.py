"""djangoproj URL Configuration"""

from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [

    # React login route
    path('login/', TemplateView.as_view(template_name="index.html")),

    # React register route (ADDED)
    path('register/', TemplateView.as_view(template_name="index.html")),

    # Django admin
    path('admin/', admin.site.urls),

    # Backend APIs
    path('djangoapp/', include('djangoapp.urls')),

    # Home page
    path('', TemplateView.as_view(template_name="Home.html")),

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
