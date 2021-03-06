"""mefi_app URL Configuration

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
from django.conf.urls import url
from django.conf.urls.static import static
from django.conf import settings
from mefi_app.views import HomeView, LoginView, ProfilePage, RegisterView

from rest_framework.routers import SimpleRouter

from .views import TagsView, EventsView, cal

tagrouter = SimpleRouter()
tagrouter.register(r'api/tags', TagsView)

eventsrouter = SimpleRouter()
eventsrouter.register(r'events', EventsView)

urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^$', HomeView.as_view()),
    url(r'^accounts/login/$', LoginView.as_view(), name="login"),
    url(r'^accounts/profile/$', ProfilePage.as_view(), name="profile"),
    url(r'^accounts/register/$', RegisterView.as_view(), name="register"),
    path('cal/', cal)
] + static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS)


urlpatterns += tagrouter.urls
urlpatterns += eventsrouter.urls