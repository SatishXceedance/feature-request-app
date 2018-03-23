from django.shortcuts import render
from django.views.generic.base import View
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models import F

from feature_request_app.serializers import ProductAreaSerializer, FeatureRequestSerializer, \
	ClientSerializer
from feature_request_app.models import Client, ProductArea, FeatureRequests
from feature_request_app.api_validators import is_client_exist, \
	is_valid_date, is_product_area_exist, is_client_priority_valid, is_client_exist


class HomePageView(View):
	"""
	This is home page view and this is for rendering home page template
	"""
	def get(self, request):		
		return render(request, 'home.html')


class FeatureRequestList(APIView):	
	"""
	This is feature request api for getting all feature requests and creating new feature requests 
	""" 
	def get(self, request, format=None):
		"""
		This is for getting feature requests and this will requrn list of all feature requests, client list, 
		and product area list
		API parameters:
			method: GET
		"""
		feature_requests_serializer = FeatureRequestSerializer(FeatureRequests.objects.all(), many=True)
		client_serializer = ClientSerializer(Client.objects.all(), many=True)
		product_area_serializer = ProductAreaSerializer(ProductArea.objects.all(), many=True)
		return Response({'feature_requests': feature_requests_serializer.data,
						'clients': client_serializer.data,
						'product_areas': product_area_serializer.data})

	def post(self, request, format=None):
		"""
		This is for creating new feature request, takes following parameters and 
		returns success response otherwise error
		API parameters:
			Required parameters:
				method: POST				
				client: integer(required)
				product_area:integer(required)
				client_priority:integer(greter than 0)(required)
				target_date: date format (yyyy-mm-dd)
			Optional parameters:
				description(optional)
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
			product_exist, response = is_product_area_exist(post_data.get('product_area'))
			if product_exist:
				product_area = response
			else:
				return response
			
			#client priority is valid or not
			is_valid_priority,response = is_client_priority_valid(post_data.get('client_priority',''))
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
				return Response('Title can not empty',	status=status.HTTP_400_BAD_REQUEST)
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

				# update client priority value by one for same client  
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


