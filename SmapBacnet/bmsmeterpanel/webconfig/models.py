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
	obj_type = models.CharField(max_length=50, choices=obj_type_choices, default='analogValue')
	inst_id = models.IntegerField(default=0)
	prop_type = models.CharField(max_length=200, default = 'presentValue')
	value_type = models.CharField(max_length=200, default = 'Energy')
	value_unit = models.CharField(max_length=200, default = 'KiloWatt-Hours')
	rate = models.IntegerField(default=30)
	wing = models.CharField(max_length=200, default = '0')
	point_floor = models.IntegerField(default=0)
	point_building = models.CharField(max_length=200, default = 'Academic Block')
	point_source = models.CharField(max_length=200, default = 'ModbusBridge')
	point_type = models.CharField(max_length=200, default = 'UPS-IN1')
	point_loadtype = models.CharField(max_length=200, default = 'UPS-IN')
	point_subloadtype = models.CharField(max_length=200, default = 'UPS-IN1')
	point_supplytype = models.CharField(max_length=200, default = 'Power')
	meterid = models.IntegerField(default=0)
