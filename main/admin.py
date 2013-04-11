# coding=UTF-8
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
	actions = ['make_push']

	def make_push(self, request, queryset):
		from APNSWrapper import *
		import binascii
		for msg in queryset:
			if msg.sent:
				continue
			if msg.device.development:
				pem = msg.app.cert_dev
			else:
				pem = msg.app.cert_dist
			wrapper = APNSNotificationWrapper("/home/mrgaolei/%s" % pem, msg.device.development)
			message = APNSNotification()
			message.token(binascii.unhexlify(msg.device.devtoken))
			message.alert(msg.alert)
			message.badge(int(msg.badge))
			message.sound(msg.sound)
			wrapper.append(message)
			if wrapper.notify():
				msg.sent = True
				msg.save()

	make_push.short_description = "发推送"

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

class AppAdmin(admin.ModelAdmin):
	list_display = ('appname', 'cert_dev', 'cert_dist', 'created')

admin.site.register(App, AppAdmin)
admin.site.register(Device, DeviceAdmin)
admin.site.register(Pmsg, PmsgAdmin)
