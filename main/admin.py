from django.contrib import admin
from main.models import *
from main.forms import PmsgForm


class DeviceAdmin(admin.ModelAdmin):
	date_hierarchy = 'updated'
	list_display = ('app', 'appversion', 'devname', 'locale', 'devmodel', 'devversion', 'pushbadge', 'pushalert', 'pushsound', 'development', 'status', 'created', 'updated')
	list_filter = [ 'app', 'locale', 'devmodel', 'development']
	search_fields = ['devname']

class PropertyInline(admin.TabularInline):
	model = Property
	extra = 1

class PmsgAdmin(admin.ModelAdmin):
	date_hierarchy = 'created'
	list_display = ('app', 'device', 'badge', 'alert', 'sound', 'sent', 'created')
	list_filter = ['sent', 'app']
	search_fields = ['alert', 'device__devname']
	exclude = ['device', 'sent']
	form = PmsgForm
	inlines = [PropertyInline]
	actions = ['make_push']

	def make_push(self, request, queryset):
		from apns import APNs, Frame, Payload
		import time
		wrapper = {}
		frames = {}
		for msg in queryset:
			if msg.sent:
				continue
			if msg.device.development:
				pem = msg.app.cert_dev
			else:
				pem = msg.app.cert_dist
			key = "%d_%d" % (msg.app.pk, msg.device.development)
			if not wrapper.has_key(key):
				wrapper[key] = APNs(cert_file="/var/www/cert/%s" % pem, use_sandbox=msg.device.development)
				frames[key] = Frame()
			#wrapper = APNSNotificationWrapper("/home/mrgaolei/%s" % pem, msg.device.development)
			custom = {}

			# property
			for ppt in msg.property_set.all():
				custom[ppt.argkey] = ppt.argvalue

			payload = Payload(alert = msg.alert, sound = msg.sound, badge = int(msg.badge), custom = custom, category = msg.category)
			frames[key].add_item(msg.device.devtoken, payload, msg.pk, time.time()+3600, 10)
			
			# property
			# for ppt in msg.property_set.all():
				#message.appendProperty(APNSProperty(str(ppt.argkey), str(ppt.argvalue)))
				#message.appendProperty(APNSProperty(ppt.argkey.encode( "UTF-8" ), ppt.argvalue.encode( "UTF-8" )))

			#wrapper[key].append(message)
			#if wrapper.notify():
			msg.sent = True
			msg.save()
		keys = wrapper.keys()
		for key in keys:
			wrapper[key].gateway_server.send_notification_multiple(frames[key])

	make_push.short_description = "发推送"

	def save_formset(self, request, form, formset, change):
		if change:
			super(PmsgAdmin, self).save_formset(request, form, formset, change)
		else:
			msgs = Pmsg.objects.filter(app_id=form['app'].value(), alert=form['alert'].value())
			instances = formset.save(commit=False)
			argkey = None
			argvalue = None
			for instance in instances:
				argkey = instance.argkey
				argvalue = instance.argvalue
				for msg in msgs:
					propt = Property()
					propt.pmsg = msg
					propt.argkey = argkey
					propt.argvalue = argvalue
					propt.save()
			return

	def save_model(self, request, obj, form, change):
		if change:
			obj.save()
		else:
			if form['locale'].value():
				devices = obj.app.device_set.filter(locale=form['locale'].value())
			else:
				devices = obj.app.device_set.all()
			for device in devices:
				msg = Pmsg()
				msg.app = obj.app
				msg.device = device
				msg.badge = obj.badge
				msg.alert = obj.alert
				msg.sound = obj.sound
				msg.category = obj.category
				msg.save()

class AppAdmin(admin.ModelAdmin):
	list_display = ('appname', 'cert_dev', 'cert_dist', 'created')

admin.site.register(App, AppAdmin)
admin.site.register(Device, DeviceAdmin)
admin.site.register(Pmsg, PmsgAdmin)
