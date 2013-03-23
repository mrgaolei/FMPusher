from django.forms import ModelForm
from main.models import *

class DeviceForm(ModelForm):
	class Meta:
		model = Device