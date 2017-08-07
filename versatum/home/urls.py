"""versatum URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
import views as home
from django.conf.urls import url

urlpatterns = [
    url(r'^$', home.homepage, name="homepage"),
    url(r'^about/$', home.about, name="about"),
    url(r'^contacts/$', home.contacts, name="contacts"),
    url(r'^help/$', home.help, name="help"),
]
