# coding=UTF-8
from django.db import models

# Create your models here.
class App(models.Model):
	appname 	= models.CharField(max_length=255, unique=True)
	appkey		= models.CharField(max_length=32)
	cert_dev	= models.CharField(max_length=50)
	cert_dist	= models.CharField(max_length=50)
	created 	= models.DateTimeField(auto_now_add=True)

	def __unicode__(self):
		return self.appname

	class Meta:
		verbose_name = "应用APP"
		verbose_name_plural = verbose_name


class Device(models.Model):
	app 		= models.ForeignKey(App, on_delete=models.PROTECT)
	appversion	= models.CharField("APP版本", max_length=25)
	devtoken	= models.CharField(max_length=64)
	devname		= models.CharField(max_length=255)
	devmodel	= models.CharField("设备", max_length=100)
	devversion	= models.CharField("设备版本", max_length=25)
	pushbadge	= models.BooleanField("角标", default = True)
	pushalert	= models.BooleanField("消息", default = True)
	pushsound	= models.BooleanField("声音", default = True)
	development	= models.BooleanField("沙箱", default = False)
	status		= models.BooleanField(default=True)
	created		= models.DateTimeField(auto_now_add=True)
	updated		= models.DateTimeField(auto_now=True)
	locale		= models.CharField("地区", max_length=10, blank=True, default='', db_index = True)

	def __unicode__(self):
		return self.devname

	class Meta:
		ordering = ['-updated']
		unique_together = ("app", "devtoken")
		verbose_name = "设备"
		verbose_name_plural = verbose_name

class Pmsg(models.Model):
	app			= models.ForeignKey(App, on_delete=models.PROTECT)
	device		= models.ForeignKey(Device, on_delete=models.PROTECT)
	badge		= models.IntegerField("角标", default = 1)
	alert		= models.CharField("信息", max_length = 200, blank = True)
	sound		= models.CharField("声音", max_length = 50, default = "default", blank = True)
	sent		= models.BooleanField("已发送", default = False)
	created		= models.DateTimeField(auto_now_add=True)
	category	= models.CharField("类别", max_length = 50, blank = True, help_text = "iOS 8 专用")

	def __unicode__(self):
		return self.alert
		return "msg %s send to %s" % (self.alert, self.device.devname)

	class Meta:
		verbose_name = "推送消息"
		verbose_name_plural = verbose_name

class Property(models.Model):
	pmsg		= models.ForeignKey(Pmsg, on_delete=models.PROTECT)
	argkey		= models.CharField("key", max_length = 40)
	argvalue	= models.CharField("value", max_length = 200)

	def __unicode__(self):
		return  self.argkey

	class Meta:
		unique_together = ("pmsg", "argkey")
