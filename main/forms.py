from django.forms import ModelForm
from main.models import *

class DeviceForm(ModelForm):
	class Meta:
		model = Device
		fields = ['app', 'appversion', 'devtoken', 'devname', 'devmodel', 'devversion', 'pushbadge', 'pushalert', 'pushsound', 'development', 'status', 'locale']