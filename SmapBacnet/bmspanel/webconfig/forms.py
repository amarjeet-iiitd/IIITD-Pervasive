from django import forms
from .models import BacnetPointModel

class PointForm(forms.ModelForm):
	class Meta:
		model = BacnetPointModel
		fields=['ip','obj_type','inst_id', 'prop_type', 'value_type', 'value_unit', 'rate', 'wing', 'point_parent', 'point_name', 'point_floor', 'point_building', 'point_source']#Add any new Metadata to be added here
