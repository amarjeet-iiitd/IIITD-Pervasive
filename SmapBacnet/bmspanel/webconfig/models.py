from django.db import models

# Create your models here.

class BacnetPointModel(models.Model):
	ip = models.GenericIPAddressField(blank=True, null=True, default='0.0.0.0', verbose_name='BACnet Device IP Address (From BACnet Scan)')
	obj_type_choices = (
        ('analogInput','analogInput'),
        ('analogOutput','analogOutput'),
        ('analogValue','analogValue'),
        ('binaryInput','binaryInput'),
        ('binaryOutput','binaryOutput'),
        ('binaryValue','binaryValue')
	)
	obj_type = models.CharField(max_length=50, choices=obj_type_choices, default='analogOutput',verbose_name='BACnet Point Object type (From BACnet Scan)')
	inst_id = models.IntegerField(default=0, verbose_name='BACnet Point Instance ID (From BACnet Scan)')
	prop_type = models.CharField(max_length=200, default = 'presentValue', verbose_name='BACnet Point Property Type (presentValue for data)')
	value_type = models.CharField(max_length=200, default = 'Temperature', verbose_name='Value Type (Metadata for Physical Parameter, eg Power)')
	value_unit = models.CharField(max_length=200, default = 'Celsius', verbose_name='Value Unit (Metadata for Physical Units, eg Watts)')
	rate = models.IntegerField(default=30, verbose_name='Polling rate')
	point_parent = models.CharField(max_length=200, default = 'AHU', verbose_name='Point Parent (Metadata required for Path, eg. 1F_AHU_B)')
	point_name = models.CharField(max_length=200, default = 'RAT', verbose_name='Point Name (Metadata required for Path, eg. RAT)')
	point_floor = models.IntegerField(default=0, verbose_name='Point Floor')
	point_building = models.CharField(max_length=200, default = 'Academic Block', verbose_name='Point Building')
	wing = models.CharField(max_length=100, default = '0', verbose_name='Point Wing')
	point_source = models.CharField(max_length=200, default = 'SC1', verbose_name='Point BACnet Source (Metadata required for Path, eg. ModbusBridge)')
	#Add any new Metadata to be added here
	
