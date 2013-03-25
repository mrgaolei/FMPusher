# -*- coding: UTF-8 -*-

import md5, sys
from django.http import Http404
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.shortcuts import render
from main.forms import DeviceForm
from main.models import App

@csrf_exempt
def device(request):
	if  request.method == 'POST':
		reload(sys)
		sys.setdefaultencoding('utf-8')
		if request.POST.__contains__("appname"):
			request.POST["app"] = App.objects.get(appname=request.POST["appname"]).pk
		if request.POST.__contains__("devicetoken"):
			request.POST["devtoken"] = request.POST["devicetoken"]
		if request.POST.__contains__("devicename"):
			request.POST["devname"] = request.POST["devicename"]
		if request.POST.__contains__("devicemodel"):
			request.POST["devmodel"] = request.POST["devicemodel"]
		if request.POST.__contains__("deviceversion"):
			request.POST["devversion"] = request.POST["deviceversion"]
		if request.POST.__contains__("pushbadge"):
			if request.POST["pushbadge"] == "enabled":
				request.POST["pushbadge"] = 1
			else:
				request.POST["pushbadge"] = 0
		if request.POST.__contains__("pushalert"):
			if request.POST["pushalert"] == "enabled":
				request.POST["pushalert"] = 1
			else:
				request.POST["pushalert"] = 0
		if request.POST.__contains__("pushsound"):
			if request.POST["pushsound"] == "enabled":
				request.POST["pushsound"] = 1
			else:
				request.POST["pushsound"] = 0
		if request.POST.__contains__("development"):
			if request.POST["development"] == "sandbox":
				request.POST["development"] = 1
			else:
				request.POST["development"] = 0
		if not request.POST.__contains__("status"):
			request.POST["status"] = 1
		f = DeviceForm(request.POST)
		device = f.save(commit=False)
		sign = request.POST['sign']
		poststr = md5.new(device.app.appname + device.app.appkey + device.appversion + device.devtoken + device.devname + device.devmodel + device.devversion).hexdigest()
		if (sign == poststr):
			f.save()
			return HttpResponse("success")
		else:
			return HttpResponse(sign)
			raise Http404
	else:
		f = DeviceForm()
		return render(request, 'main/device.html', {'form': f})