from rest_framework import status
from feature_request_app.models import Client, ProductArea, FeatureRequests
from feature_request_app.serializers import FeatureRequestSerializer
from rest_framework.response import Response
import datetime


#client validation
def is_client_exist(client_id):
	# client id must be isteger
	try:
		client_id = int(client_id)
	except ValueError as ex:
		response = Response('Clint Id Must Be Integer', 
						status=status.HTTP_400_BAD_REQUEST)	
		return (False, response)
	# check client exist or not	
	try:
		client = Client.objects.get(pk=client_id)
		return (True, client)
	except Client.DoesNotExist:
		response = Response('Client not found', status=status.HTTP_404_BAD_REQUEST)
		return (False, response)

# product area validation
def is_product_area_exist(product_area_id):
	#product area id must be integer
	try:
		product_area_id = int(product_area_id)
	except ValueError as ex:
		response = Response('Product Id Must Be Integer', 
						status=status.HTTP_400_BAD_REQUEST)	
		return (False, response)
	# check product area exist or not	
	try:
		product_area = ProductArea.objects.get(pk=product_area_id)
		return (True, product_area)
	except ProductArea.DoesNotExist:
		response = Response('Product Area Not Found', 
								status=status.HTTP_404_BAD_REQUEST)
		return (False, response)

#client priority validation
def is_client_periority_valid(client_priority):
	# priority must be integer
	try:
		client_priority = int(client_priority)
		# priority mut be greater than 0
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
	# target date format validation
	try:
		target_date = datetime.datetime.strptime(target_date, '%Y-%m-%d')
		# target date must be greater than today's date
		if datetime.datetime.now() <= target_date:
			return (True, target_date)
		else:
			response = Response('Target date has gone',
						status=status.HTTP_400_BAD_REQUEST)
	except ValueError:
		response = Response('Incorrect Date Formate',
						status=status.HTTP_400_BAD_REQUEST)
	return (False, response)