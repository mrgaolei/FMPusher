import md5
from django.http import Http404
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.shortcuts import render
from main.forms import DeviceForm

@csrf_exempt
def device(request):
	if  request.method == 'POST':
		f = DeviceForm(request.POST)
		device = f.save(commit=False)
		sign = request.POST['sign']
		poststr = md5.new(device.app.appname + device.appversion + device.devtoken + device.devname + device.devmodel + device.devversion).hexdigest()
		if (sign == poststr):
			f.save()
			pass
		else:
			raise Http404
	else:
		f = DeviceForm()
		return render(request, 'main/device.html', {'form': f})