from django.db import models

# Create your models here.
from django.db import models

from django.core.validators import MinValueValidator



class Client(models.Model):
	name = models.CharField(max_length=30, unique=True)


class Product_Area(models.Model):
	name = models.CharField(max_length=30, unique=True)


class Feature_Requests(models.Model):
	title = models.CharField(max_length=30)
	description = models.TextField()
	client = models.ForeignKey('Client', on_delete=models.CASCADE)
	client_priority = models.IntegerField(default=1,
									    validators=[MinValueValidator(1)]
									    )
	target_date = models.DateTimeField(blank=True, null=True)   
	product_area = models.ForeignKey('Product_Area', on_delete=models.CASCADE)

