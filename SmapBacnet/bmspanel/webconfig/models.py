from django.db import models

# Create your models here.

class BacnetPointModel(models.Model):
	ip = models.GenericIPAddressField(blank=True, null=True, default='0.0.0.0')
	obj_type_choices = (
        ('analogInput','analogInput'),
        ('analogOutput','analogOutput'),
        ('analogValue','analogValue'),
        ('binaryInput','binaryInput'),
        ('binaryOutput','binaryOutput'),
        ('binaryValue','binaryValue')
	)
	value_type_choices = (
        ('analogInput','analogInput'),
        ('analogOutput','analogOutput'),
        ('analogValue','analogValue'),
        ('binaryInput','binaryInput'),
        ('binaryOutput','binaryOutput'),
        ('binaryValue','binaryValue')
	)
	obj_type = models.CharField(max_length=50, choices=obj_type_choices, default='analogOutput')
	inst_id = models.IntegerField(default=0)
	prop_type = models.CharField(max_length=200, default = 'presentValue')
	value_type = models.CharField(max_length=200, default = 'Temperature')
	value_unit = models.CharField(max_length=200, default = 'Celsius')
	rate = models.IntegerField(default=30)
	point_parent = models.CharField(max_length=200, default = 'AHU')
	point_name = models.CharField(max_length=200, default = 'RAT')
	point_floor = models.IntegerField(default=0)
	point_building = models.CharField(max_length=200, default = 'Academic Block')
	point_source = models.CharField(max_length=200, default = 'SC1')
	
