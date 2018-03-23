from django.urls import path

from rest_framework.urlpatterns import format_suffix_patterns
from . import views



urlpatterns = [
	path('feature_request_list/', views.FeatureRequestList.as_view(), 
								name='feature_request_list'),
	path('', views.HomePageView.as_view(), name='home'),
]

urlpatterns = format_suffix_patterns(urlpatterns)