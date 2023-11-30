"""
URL configuration for mysite project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin, admindocs
from django.urls import path, include
from django.conf.urls.i18n import i18n_patterns
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView

from django.contrib.sitemaps.views import sitemap
from .sitemaps import sitmaps

urlpatterns = [
    # path('admin/', admin.site.urls),
    # path('shop/', include('shopapp.urls')),
    # path('', include('shopapp.urls')),
    path('req/', include('requestdataapp.urls')),
    path('accounts/', include('myauth.urls')),
    path("sitemap.xml", sitemap, {"sitemaps": sitmaps}, name="django.contrib.sitemaps.views.sitemap")

]

urlpatterns += i18n_patterns(
    path('admin/doc/', include('django.contrib.admindocs.urls')),
    path('admin/', admin.site.urls),
    path('shop/', include('shopapp.urls')),
    path('', include('shopapp.urls')),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/schema/swagger/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger_schema'),
    path('api/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc_schema'),
    path('articles/', include('blogapp.urls')),
)

if settings.DEBUG:
    urlpatterns.extend(
        static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    )
    urlpatterns.append(
        path("__debug__/", include("debug_toolbar.urls")),
    )
