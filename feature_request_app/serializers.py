from rest_framework import serializers

from feature_request_app.models import Client, Product_Area, Feature_Requests


class FeatureRequestSerializer(serializers.ModelSerializer):
	client_name = serializers.ReadOnlyField(source="client.name")
	product_area_name = serializers.ReadOnlyField(source="product_area.name")

	class Meta:

		model = Feature_Requests
		fields = ('id', 'title', 'description', 'client_priority', 'target_date', 'client_name', 
				'product_area_name',)

	# def create(self, validated_data):
	# 	"""
	# 	Create and return a new  instance, given the validated data.
	# 	"""
	# 	return Feature_Requests.objects.create(**validated_data)



# from feature_request_app.models import Client, Product_Area, Feature_Requests
# from feature_request_app.serializers import FeatureRequestSerializer
# serializer = FeatureRequestSerializer(Feature_Requests.objects.all()[0])
# serializer.data