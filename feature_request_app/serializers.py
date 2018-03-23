from rest_framework import serializers
from feature_request_app.models import Client, ProductArea, FeatureRequests



class FeatureRequestSerializer(serializers.ModelSerializer):
	"""
	Feature request data serializer
	"""
	#get client 
	client_name = serializers.ReadOnlyField(source="client.name")
	# get product area 
	product_area_name = serializers.ReadOnlyField(source="product_area.name")

	class Meta:
		model = FeatureRequests
		fields = ('id', 'title', 'description', 'client_priority', 'target_date', 
			'client_name', 'product_area_name',)


class ClientSerializer(serializers.ModelSerializer):
	"""
	client data serializer
	"""
	class Meta:
		model = Client
		fields = ('id', 'name',)


class ProductAreaSerializer(serializers.ModelSerializer):
	"""
	product-area data serializer
	"""

	class Meta:
		model = ProductArea
		fields = ('id', 'name',)

