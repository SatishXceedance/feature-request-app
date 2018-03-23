from django.db import models

from django.core.validators import MinValueValidator
from django.utils import timezone



# client table
class Client(models.Model):
	name = models.CharField(max_length=30, unique=True)

	
# product area table
class ProductArea(models.Model):
	name = models.CharField(max_length=30, unique=True)


# feature request table
class FeatureRequests(models.Model):
	title = models.CharField(max_length=30)
	description = models.TextField()
	client = models.ForeignKey('Client', on_delete=models.CASCADE)
	client_priority = models.IntegerField(default=1,
			validators=[MinValueValidator(1)]
		)
	target_date = models.DateTimeField(blank=True, null=True)   
	product_area = models.ForeignKey('ProductArea', on_delete=models.CASCADE)

