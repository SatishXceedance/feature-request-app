from rest_framework import serializers
from feature_request_app.models import Client, ProductArea, FeatureRequests


# Feature request data serializer
class FeatureRequestSerializer(serializers.ModelSerializer):
	client_name = serializers.ReadOnlyField(source="client.name")
	product_area_name = serializers.ReadOnlyField(source="product_area.name")

	class Meta:
		model = FeatureRequests
		fields = ('id', 'title', 'description', 'client_priority', 'target_date', 
			'client_name', 'product_area_name',)


# client data serializer
class ClientSerializer(serializers.ModelSerializer):

	class Meta:
		model = Client
		fields = ('id', 'name',)


# product-area data serializer
class ProductAreSerializer(serializers.ModelSerializer):

	class Meta:
		model = ProductArea
		fields = ('id', 'name',)

