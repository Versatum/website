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

import views
from utils import HandleError
from django.contrib import admin
from django.conf.urls import url, include

handler400 = HandleError(status_code=400)
handler403 = HandleError(status_code=403)
handler404 = HandleError(status_code=404)
handler500 = HandleError(status_code=500)

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^login/$', views.login, name="login"),
    url(r'^logout/$', views.logout, name='logout'),
    url(r'^register/$', views.register, name="register"),
    url(r'^confirm/(?P<string>[\w\W]+)/$', views.confirm, name="confirm"),
    url(r'^', include("home.urls", namespace="home")),
    url(r'^project/', include("project.urls", namespace="project")),
    url(r'^blog/', include("blog.urls", namespace="blog")),
]
