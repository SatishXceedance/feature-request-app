from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse

from django.views.generic import TemplateView
from django.db.models import F
from django.conf.urls import handler404
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from feature_request_app.models import Client, Product_Area, Feature_Requests
from feature_request_app.serializers import FeatureRequestSerializer
import datetime


def home_page(request):
	clients_list = Client.objects.all()
	product_area_list = Product_Area.objects.all()
	return render(request, 'home.html', {'clients_list': clients_list,
										'product_area_list':product_area_list})

@api_view()
def error_page(request):
    return Response({'detail': 'Not found'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET', 'POST'])
def feature_request_list(request, format=None):
	"""
	List all code featuer request, or create a new request.
	"""
	if request.method == 'GET':
		feature_requests = Feature_Requests.objects.all()
		serializer = FeatureRequestSerializer(feature_requests, many=True)
		return Response(serializer.data)

	elif request.method == 'POST':		
		post_data = request.POST.copy()
		try:
			cliest_exist, response = is_client_exist(post_data.get('client'))
			if cliest_exist:
				client = response
			else:
				return response

			product_exist, response = is_product_area_exist(post_data.get('product_area'))
			if product_exist:
				product_area = response
			else:
				return response
			
			is_valid_priority,response = is_client_periority_valid(
									post_data.get('client_priority',''))
			if is_valid_priority:
				client_priority = response
			else:
				return response
			
			is_valid, response = is_valid_date(post_data.get('target_date',''))
			if is_valid:
				target_date = response
			else:
				return response
			title = post_data.get('title','')
			if title == "":
				return Response('Title can not empty', 
						status=status.HTTP_400_BAD_REQUEST)
			description = post_data.get('description','')
			try:					
				request_obj = Feature_Requests.objects.create(title=title,
											description=description,
											client=client,
											product_area=product_area,
											client_priority=client_priority,
											target_date=target_date)
				req_objs = Feature_Requests.objects.filter(
								client=client,
								client_priority__gte=client_priority)
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


#client validation
def is_client_exist(client_id):
	try:
		client_id = int(client_id)
	except ValueError as ex:
		response = Response('Clint Id Must Be Integer', 
						status=status.HTTP_400_BAD_REQUEST)	
		return (False, response)	
	try:
		client = Client.objects.get(pk=client_id)
		return (True, client)
	except Client.DoesNotExist:
		response = Response('Client not found', status=status.HTTP_400_BAD_REQUEST)
		return (False, response)

# product area validation
def is_product_area_exist(product_area_id):
	try:
		product_area_id = int(product_area_id)
	except ValueError as ex:
		response = Response('Product Id Must Be Integer', 
						status=status.HTTP_400_BAD_REQUEST)	
		return (False, response)	
	try:
		product_area = Product_Area.objects.get(pk=product_area_id)
		return (True, product_area)
	except Product_Area.DoesNotExist:
		response = Response('Product Area Not Found', status=status.HTTP_400_BAD_REQUEST)
		return (False, response)

#client priority validation
def is_client_periority_valid(client_priority):
	try:
		client_priority = int(client_priority)
		if not client_priority > 0:
			response = Response('Client Periority Must Be Positive', 
						status=status.HTTP_400_BAD_REQUEST)
		else:
			return (True, client_priority) 
	except ValueError as ex:
		response = Response('Client Periority Must Be Integer', 
						status=status.HTTP_400_BAD_REQUEST)	
	return (False, response)

#target date validation
def is_valid_date(target_date):
	try:
		target_date = datetime.datetime.strptime(target_date, '%d-%m-%Y')
		if datetime.datetime.now() <= target_date:
			return (True, target_date)
		else:
			response = Response('Target date has gone',
						status=status.HTTP_400_BAD_REQUEST)
	except ValueError:
		response = Response('Incorrect Date, Should Be DD-MM-YYYY',
						status=status.HTTP_400_BAD_REQUEST)
	return (False, response)