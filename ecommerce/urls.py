"""ecommerce URL Configuration
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
from django.urls import path, include

from django.conf.urls.static import static
from django.conf import settings #gives us access to media url

#importing login
from django.contrib.auth import views as auth_views

from store import views as store_views
#store is the app name and store_views can be named anything we want

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('store.urls')),

    path('register/', store_views.register, name='register'),
#login/logout
    path('login/', auth_views.LoginView.as_view(template_name='store/login.html'),name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='store/logout.html'),name='logout')
]

urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
#appending to the list