from rest_framework import status
from feature_request_app.models import Client, ProductArea, FeatureRequests
from feature_request_app.serializers import FeatureRequestSerializer
import datetime


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
		product_area = ProductArea.objects.get(pk=product_area_id)
		return (True, product_area)
	except ProductArea.DoesNotExist:
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