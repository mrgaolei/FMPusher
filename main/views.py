# -*- coding: UTF-8 -*-

import hashlib, sys
from django.http import Http404
from django.shortcuts import get_list_or_404, get_object_or_404, redirect
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.shortcuts import render
from main.forms import DeviceForm
from main.models import *

def home(request):
	return redirect('/admin/')

@csrf_exempt
def device(request):
	if  request.method == 'POST':
		reload(sys)
		sys.setdefaultencoding('utf-8')
		formdata = request.POST.copy()
		if request.POST.__contains__("appname"):
			app = App.objects.get(appname=request.POST["appname"])
			formdata["app"] = app.pk
		else:
			app = App.objects.get(pk=request.POST["app"])
		if request.POST.__contains__("devicetoken"):
			formdata["devtoken"] = request.POST["devicetoken"]
		if request.POST.__contains__("locale"):
			formdata["locale"] = request.POST["locale"]
		else:
			formdata["locale"] = "unknow"
		if request.POST.__contains__("devicename"):
			formdata["devname"] = request.POST["devicename"]
		if request.POST.__contains__("devicemodel"):
			formdata["devmodel"] = request.POST["devicemodel"]
		if request.POST.__contains__("deviceversion"):
			formdata["devversion"] = request.POST["deviceversion"]
		if request.POST.__contains__("pushbadge"):
			if request.POST["pushbadge"] == "enabled":
				formdata["pushbadge"] = 1
			else:
				formdata["pushbadge"] = 0
		if request.POST.__contains__("pushalert"):
			if request.POST["pushalert"] == "enabled":
				formdata["pushalert"] = 1
			else:
				formdata["pushalert"] = 0
		if request.POST.__contains__("pushsound"):
			if request.POST["pushsound"] == "enabled":
				formdata["pushsound"] = 1
			else:
				formdata["pushsound"] = 0
		if request.POST.__contains__("development"):
			if request.POST["development"] == "sandbox":
				formdata["development"] = 1
			else:
				formdata["development"] = 0
		if not request.POST.__contains__("status"):
			formdata["status"] = 1
		try:
			existsDev = Device.objects.get(app=app,devtoken=formdata["devtoken"])
			f = DeviceForm(formdata, instance=existsDev)
		except Device.DoesNotExist:
			f = DeviceForm(formdata)
		device = f.save(commit=False)
		sign = request.POST['sign']
		poststr = hashlib.md5().update(device.app.appname + device.app.appkey + device.appversion + device.devtoken + device.devname + device.devmodel + device.devversion).hexdigest()
		if (sign == poststr):
			f.save()
			return HttpResponse("success")
		else:
			raise Http404
	else:
		f = DeviceForm()
		return render(request, 'main/device.html', {'form': f})


def clkcount(request, url):
	if not url[0:4] == 'http':
		url = 'http://' + url
	try:
		tc = Tscount.objects.get(url=url)
		tc.num += 1
	except Exception as e:
		tc = Tscount()
		tc.url = url
	tc.save()
	return redirect(url)

def clkcountpk(request, pk):
	try:
		tc = Tscount.objects.get(pk=pk)
		tc.num += 1
	except Exception as e:
		pass
	tc.save()
	return redirect(tc.url)