"""
URL configuration for auth_server project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.urls import path,include
from django.shortcuts import render

def profile_view(request):
    return render(request, 'profile.html')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('oidc/', include('oidc_provider.urls', namespace='oidc_provider')),
    path('accounts/', include('django.contrib.auth.urls')),  # <-- Agregar esta línea
    path('accounts/profile/', profile_view, name='profile'),
]