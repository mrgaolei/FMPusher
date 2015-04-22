# coding=UTF-8
from django import forms
from django.forms import ModelForm
from main.models import *

class DeviceForm(ModelForm):
	class Meta:
		model = Device
		fields = ['app', 'appversion', 'devtoken', 'devname', 'devmodel', 'devversion', 'pushbadge', 'pushalert', 'pushsound', 'development', 'status', 'locale']

class PmsgForm(ModelForm):
	locale = forms.CharField(label="地区", max_length=10,help_text='若要推送给全部用户，请留空',required=False)
	class Meta:
		model = Pmsg
		fields = ['app', 'badge', 'alert', 'sound', 'category']