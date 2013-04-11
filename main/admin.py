from django.contrib import admin
from main.models import *

class DeviceAdmin(admin.ModelAdmin):
	date_hierarchy = 'updated'
	list_display = ('app', 'appversion', 'devname', 'devmodel', 'devversion', 'pushbadge', 'pushalert', 'pushsound', 'development', 'status', 'created', 'updated')
	list_filter = [ 'app', 'devmodel', 'development']
	search_fields = ['devname']

class PmsgAdmin(admin.ModelAdmin):
	date_hierarchy = 'created'
	list_display = ('app', 'device', 'badge', 'alert', 'sound', 'sent', 'created')
	search_fields = ['alert']
	exclude = ['device', 'sent']

	def save_model(self, request, obj, form, change):
		devices = obj.app.device_set.all()
		for device in devices:
			msg = Pmsg()
			msg.app = obj.app
			msg.device = device
			msg.badge = obj.badge
			msg.alert = obj.alert
			msg.sound = obj.sound
			msg.save()


admin.site.register(App)
admin.site.register(Device, DeviceAdmin)
admin.site.register(Pmsg, PmsgAdmin)
