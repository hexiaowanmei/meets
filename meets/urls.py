"""meets URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from django.contrib.staticfiles.urls import static
from meets.settings import MEDIA_URL, MEDIA_ROOT


urlpatterns = [
    path('admin/', admin.site.urls),
    path('homepage/', include(('homepage.urls', 'homepage'), namespace='homepage')),
    path('backstage/', include(('backstage.urls', 'backstage'), namespace='backstage')),
    path('user/', include(('user.urls', 'user'), namespace='user')),
    path('information/', include(('information.urls', 'information'), namespace='information')),
    path('dynamictalk/', include(('dynamictalk.urls', 'dynamictalk'), namespace='dynamictalk')),
    path('gauge_point/', include(('gauge_point.urls', 'gauge_point'), namespace='gauge_point')),


]
urlpatterns += static(MEDIA_URL, document_root=MEDIA_ROOT)
