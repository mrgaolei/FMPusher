# coding=UTF-8
from django.db import models

# Create your models here.
class App(models.Model):
	appname 	= models.CharField(max_length=255, unique=True)
	appkey		= models.CharField(max_length=32)
	created 	= models.DateTimeField(auto_now_add=True)

	def __unicode__(self):
		return self.appname


class Device(models.Model):
	app 		= models.ForeignKey(App)
	appversion	= models.CharField("APP版本", max_length=25)
	devtoken	= models.CharField(max_length=64)
	devname		= models.CharField(max_length=255)
	devmodel	= models.CharField("设备", max_length=100)
	devversion	= models.CharField("设备版本", max_length=25)
	pushbadge	= models.BooleanField("角标")
	pushalert	= models.BooleanField("消息")
	pushsound	= models.BooleanField("声音")
	development	= models.BooleanField("沙箱")
	status		= models.BooleanField(default=True)
	created		= models.DateTimeField(auto_now_add=True)
	updated		= models.DateTimeField(auto_now=True)

	def __unicode__(self):
		return self.devname

	class Meta:
		ordering = ['-updated']
		unique_together = ("app", "devtoken")

class Pmsg(models.Model):
	device		= models.ForeignKey(Device)
	badge		= models.CharField("角标", max_length = 3, default = "1", blank = True)
	alert		= models.CharField("信息", max_length = 200, blank = True)
	sound		= models.CharField("声音", max_length = 50, default = "default", blank = True)
	sent		= models.BooleanField("已发送", default = False)
	created		= models.DateTimeField(auto_now_add=True)

	def __unicode__(self):
		return "msg %s send to %s" % (self.alert, self.device.devname)