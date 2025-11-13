"""
URL configuration for cs412 project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
# cs412/urls.py
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView
from django.contrib.auth import views as auth_views
from dadjokes import urls as dj_urls


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('quotes.urls', namespace='quotes')),
    path('restaurant/', include(('restaurant.urls', 'restaurant'), namespace='restaurant')),
    path("mini_insta/", include(("mini_insta.urls", "mini_insta"), namespace="mini_insta")),
    path('login/', auth_views.LoginView.as_view(template_name='mini_insta/login.html'), name='login'), 
	path('logout/', auth_views.LogoutView.as_view(next_page='mini_insta:show_all_profiles'), name='logout'),
    #path('voter_analytics/', include(('voter_analytics.urls', 'voter_analytics'), namespace='voter_analytics')),
    path('dadjokes/', include((dj_urls.html_urlpatterns, 'dadjokes'), namespace='dadjokes')),
    path('api/', include((dj_urls.api_urlpatterns, 'dadjokes_api'), namespace='dadjokes_api')),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)