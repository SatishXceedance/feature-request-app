from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic.base import View
from django.views.generic import TemplateView
from django.conf.urls import handler404
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models import F

from feature_request_app.serializers import ProductAreaSerializer, \
					FeatureRequestSerializer, ClientSerializer
from feature_request_app.models import Client, ProductArea, FeatureRequests
from feature_request_app.api_validators import is_client_exist, \
	is_valid_date, is_product_area_exist, is_client_periority_valid, is_client_exist
import datetime



class HomePageView(View):
	"""
	Home page view
	"""
	def get(self, request):		
		return render(request, 'home.html')


# feature request api
class FeatureRequestList(APIView):	
	"""
    List all requests, or create a new request.

	""" 
	def get(self, request, format=None):
		"""
			get all feature requests with client list and product area list
		"""
		feature_requests_serializer = FeatureRequestSerializer(
										FeatureRequests.objects.all(), many=True)
		client_serislizer = ClientSerializer(Client.objects.all(), many=True)
		product_area_serializer = ProductAreaSerializer(ProductArea.objects.all(), 
									many=True)
		return Response({'feature_requests': feature_requests_serializer.data,
						'clients': client_serislizer.data,
						'product_areas': product_area_serializer.data})

	def post(self, request, format=None):
		"""
		create new feature request
		"""
		serializer = FeatureRequestSerializer(data=request.data)
		post_data = request.POST.copy()
		try:
			# client exist or not 
			cliest_exist, response = is_client_exist(post_data.get('client'))
			if cliest_exist:
				client = response
			else:
				return response

			# product area exist or not 
			product_exist, response = is_product_area_exist(post_data.get(
															'product_area'))
			if product_exist:
				product_area = response
			else:
				return response
			
			#client periority is valid or not
			is_valid_priority,response = is_client_periority_valid(
									post_data.get('client_priority',''))
			if is_valid_priority:
				client_priority = response
			else:
				return response
			
			#target date is valid or not
			is_valid, response = is_valid_date(post_data.get('target_date',''))
			if is_valid:
				target_date = response
			else:
				return response

			# title is available or not
			title = post_data.get('title','')
			if title == "":
				return Response('Title can not empty', 
						status=status.HTTP_400_BAD_REQUEST)
			description = post_data.get('description','')
			try:					
				request_obj = FeatureRequests.objects.create(title=title,
											description=description,
											client=client,
											product_area=product_area,
											client_priority=client_priority,
											target_date=target_date)

				# get feature requests with same periority for same cliient
				req_objs = FeatureRequests.objects.filter(
								client=client,
								client_priority__gte=client_priority)

				# update client periority value by one for same client  
				req_objs.exclude(id=request_obj.id).update(
									client_priority=F('client_priority')+1)
				if request_obj:
					return Response("Request created successfully", 
									status=status.HTTP_201_CREATED)
			except:
				return Response('Request not created', 
								status=status.HTTP_400_BAD_REQUEST)
		except:
			return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


