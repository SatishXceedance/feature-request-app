from django.test import TestCase, Client
from rest_framework import status
from django.urls import reverse
from feature_request_app.models import ProductArea, FeatureRequests
from feature_request_app.models import Client as client_table
import json

# initialize the APIClient app
client = Client()


class FeatureRequestsTests(TestCase):
    """
    initialize feature requests api test cases
    """
    def setUp(self):
        """
        setup to get and create feature requests
        """
        client_obj = client_table.objects.create(name="test_client")
        product_area_obj = ProductArea.objects.create(name="test_product_area")

    def test_get_data(self):
        """
        Ensure we can get all requests objects.
        """
        url = reverse('feature_request_list')
        response = client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_post_data(self):
        """
        Ensure we can create a new request object.
        """
        url = reverse('feature_request_list')
        client_obj = client_table.objects.get(name='test_client')
        product_area_obj = ProductArea.objects.get(name='test_product_area')
        data = {'client': client_obj.id,
                'product_area': product_area_obj.id,
                'client_priority': 1,
                'target_date': '12-12-2018',
                'title': 'testing',
                'description': 'this is for testing'}
        response = client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(FeatureRequests.objects.count(), 1)
        self.assertEqual(FeatureRequests.objects.get().title, 'testing')
        