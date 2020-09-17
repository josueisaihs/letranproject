"""Bartolo URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path
from django.contrib.auth import views as auth_views
from django.conf.urls.static import static
from django.conf.urls import handler404, handler500, handler403
from django.conf import settings
from django.contrib.sitemaps.views import sitemap
from django.views.generic.base import TemplateView
from django.views.decorators.cache import cache_page

import debug_toolbar

from Docencia.sitemaps import Dynamic

sitemaps = {
    "dynamic": Dynamic
}


urlpatterns = [
    # Admin
    path('jet/', include('jet.urls', 'jet')),
    path('jet/dashboard/', include('jet.dashboard.urls', 'jet-dashboard')),
    path('admin/', admin.site.urls),

    # Aplicacion
    path('docencia/', include('Docencia.urls')),
    path('', include('Docencia.urls')),
    path("ckeditor5/", include('django_ckeditor_5.urls')),
    
    # Social Auth
    path('social/', include('social_django.urls', namespace='social')),
    # Autentificacion
    path("login/", auth_views.LoginView.as_view(), name="login"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path('pwdreset/', auth_views.PasswordResetView.as_view(), name='pwdreset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done',),
    path('password_reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm',),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete',),
    path('__debug__/', include(debug_toolbar.urls)),

    path('sitemap.xml', cache_page(60 * 60)(sitemap), {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
    path('robots.txt', cache_page(60 * 60)(TemplateView.as_view(template_name="robots.txt", content_type="text/plain"))),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = 'Docencia.views.pag_404_not_found'
handler500 = 'Docencia.views.pag_500_error_server'
handler403 = 'Docencia.views.pag_403_permission_denied'