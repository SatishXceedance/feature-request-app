from rest_framework import status
from feature_request_app.models import Client, ProductArea, FeatureRequests
from feature_request_app.serializers import FeatureRequestSerializer
from rest_framework.response import Response
import datetime


def is_client_exist(client_id):
	"""
	This will check client type, and client existance in database
	"""
	# client id must be integer
	try:
		client_id = int(client_id)
	except ValueError as ex:
		response = Response('Client Id Must Be Integer', status=status.HTTP_400_BAD_REQUEST)	
		return (False, response)
	# check client exist or not	
	try:
		client = Client.objects.get(pk=client_id)
		return (True, client)
	except Client.DoesNotExist:
		response = Response('Client not found', status=status.HTTP_404_BAD_REQUEST)
		return (False, response)

def is_product_area_exist(product_area_id):
	"""
	This will check product area type, and type is valid than check data existance in database 
	"""
	try:
		product_area_id = int(product_area_id)
	except ValueError as ex:
		response = Response('Product Id Must Be Integer', status=status.HTTP_400_BAD_REQUEST)	
		return (False, response)
	# check product area exist or not	
	try:
		product_area = ProductArea.objects.get(pk=product_area_id)
		return (True, product_area)
	except ProductArea.DoesNotExist:
		response = Response('Product Area Not Found', status=status.HTTP_404_BAD_REQUEST)
		return (False, response)

def is_client_priority_valid(client_priority):
	"""
	This will check that client priority is integer or not and also check that 
	priority should be greater than 0
	"""
	# priority must be integer
	try:
		client_priority = int(client_priority)
		# priority mut be greater than 0
		if not client_priority > 0:
			response = Response('Client Priority Must Be Greater Than 0)', 
				status=status.HTTP_400_BAD_REQUEST)
		else:
			return (True, client_priority) 
	except ValueError as ex:
		response = Response('Client Priority Must Be Integer', status=status.HTTP_400_BAD_REQUEST)	
	return (False, response)

def is_valid_date(target_date):
	"""
	This will check target date is valid or not and also check the date format
	"""
	# target date format validation
	try:
		target_date = datetime.datetime.strptime(target_date, '%d-%m-%Y')
		# target date must be greater than or equal to today's date
		if datetime.datetime.now().date() <= target_date.date():
			return (True, target_date)
		else:
			response = Response('Target Date Not Valid', status=status.HTTP_400_BAD_REQUEST)
	except ValueError:
		response = Response('Incorrect Date Format', status=status.HTTP_400_BAD_REQUEST)
	return (False, response)