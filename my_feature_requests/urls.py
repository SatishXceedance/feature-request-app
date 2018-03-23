from django.contrib import admin
from django.urls import path, include

from feature_request_app import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('feature_request_app.urls')),
]
