"""photo_blog URL Configuration

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
from django.urls import path
from django.conf.urls import include, url
from django.conf import settings            # for images/media line below
from django.conf.urls.static import static  # ditto
from blog import urls as blog_urls
from profiles import urls as profiles_urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", include(blog_urls, namespace="blog")),
    path("profile/", include(profiles_urls, namespace="profiles")),
    url("", include("allauth.urls")),      
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)    # this connects "media" file storage to the "media" url (see settings.py); dev only
