from django.contrib import admin
from django.urls import path,include
from api import urls as email_urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path('email/',include(email_urls))
]
