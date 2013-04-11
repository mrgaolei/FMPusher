from django.contrib import admin
from main.models import *

class DeviceAdmin(admin.ModelAdmin):
	date_hierarchy = 'updated'
	list_display = ('app', 'appversion', 'devname', 'devmodel', 'devversion', 'pushbadge', 'pushalert', 'pushsound', 'development', 'status', 'created', 'updated')
	list_filter = [ 'app', 'devmodel', 'development']
	search_fields = ['devname']

class PmsgAdmin(admin.ModelAdmin):
	date_hierarchy = 'created'
	list_display = ('device', 'badge', 'alert', 'sound', 'sent', 'created')
	search_fields = ['alert']

admin.site.register(App)
admin.site.register(Device, DeviceAdmin)
<<<<<<< HEAD
=======
admin.site.register(Pmsg, PmsgAdmin)
>>>>>>> be6ff5294d17d6b912d8ec0223a11d69d29e72b1
