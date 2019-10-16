"""tsmt URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
admin.autodiscover()
from django.urls import path
from django.conf.urls import include, url
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls.i18n import i18n_patterns

urlpatterns = [
    url(r'^$', views.index),
    url(r'^about$', views.about),
    url(r'^stellar/', include('stellar.urls')),
    url(r'^settings/', views.settings),
    url(r'^admin/', admin.site.urls),
    url(r'^register/update', views.register_update),
    url(r'^register/', views.register),
    url(r'^remittance/', views.remittance),
    url(r'^login_user/', views.login_user),
    url(r'^logout_user/', views.logout_user),
    url(r'^set_mycookie/', views.set_mycookie),
    url(r'^i18n/', include('django.conf.urls.i18n')),
]
if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL,
                              document_root=settings.MEDIA_ROOT)