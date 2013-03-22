from django.db import models

# Create your models here.
class App(models.Model):
	appname 	= models.CharField(max_length=255)
	appkey		= models.CharField(max_length=32)
	created 	= models.DateTimeField(auto_now_add=True)

class Device(models.Model):
	app 		= models.ForeignKey(App)
	appversion	= models.CharField(max_length=25)
	devtoken	= models.CharField(max_length=64)
	devname		= models.CharField(max_length=255)
	devmodel	= models.CharField(max_length=100)
	devversion	= models.CharField(max_length=25)
	pushbadge	= models.BooleanField()
	pushalert	= models.BooleanField()
	pushsound	= models.BooleanField()
	development	= models.BooleanField()
	status		= models.BooleanField()
	created		= models.DateTimeField(auto_now_add=True)
	updated		= models.DateTimeField(auto_now=True)