from django.contrib import admin
from django.urls import path,include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('social.urls')),
    path('',include('django.contrib.auth.urls')), # to add default django auth system viesw
]
