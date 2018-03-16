from django.urls import path

from rest_framework.urlpatterns import format_suffix_patterns
from . import views

urlpatterns = [
    path('feature_request_list/', views.feature_request_list, 
    	name='feature_request_list'),
	path('', views.home_page, name='home'),    

]


urlpatterns = format_suffix_patterns(urlpatterns)