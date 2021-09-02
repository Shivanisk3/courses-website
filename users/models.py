from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.exceptions import ObjectDoesNotExist
from django import forms
import datetime

# Create your models here.
#class form(models.Model):
#	username = models.CharField(max_length=100)
#	email_address = models.CharField(max_length=100)
#
#class Reg(models.Model):
#	username = models.CharField(max_length=100)
#	email_address = models.EmailField(primary_key=True)
#	password = models.CharField(max_length=100)

	#def __str__(self):
	#	return self.user.username

class Section(models.Model):
	sec_name = models.CharField(max_length=100)
	cover_pic = models.FileField(upload_to="media/%Y/%m/%d")
	description = models.TextField()
	added_on = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.sec_name

class register_table(models.Model):
	user = models.OneToOneField(User,on_delete=models.CASCADE)
	contact_number = models.IntegerField(default=0)
	profile_pic = models.ImageField(upload_to="profiles/%Y/%m/%d",null=True,blank=True)
	about = models.TextField(blank=True,null=True)
	occupation = models.CharField(max_length=250,null=True,blank=True)
	added_on =models.DateTimeField(auto_now_add=True,null=True)
	update_on = models.DateTimeField(auto_now=True,null=True)

	def __str__(self):
		return self.user.username

@receiver(post_save, sender=User)
def update_user_profile(sender, instance, created, **kwargs):
	try:
		instance.register_table.save()
	except ObjectDoesNotExist:
		register_table.objects.create(user=instance)
	#if created:
	#	register_table.objects.create(user=instance)
	#instance.register_table.save()

class add_course(models.Model):
	tutor = models.ForeignKey(User,on_delete=models.CASCADE)
	course_name = models.CharField(max_length=250)
	course_section = models.ForeignKey(Section,on_delete = models.CASCADE )
	course_price = models.FloatField()
	sale_price = models.CharField(max_length=200)
	course_image = models.ImageField(upload_to="courses/%Y/%m/%d")
	details = models.TextField()

	def __str__(self):
		return self.course_name

class cart(models.Model):
	user = models.ForeignKey(User,on_delete = models.CASCADE)
	course = models.ForeignKey(add_course,on_delete = models.CASCADE)
	status = models.BooleanField(default=False)
	added_on =models.DateTimeField(auto_now_add=True,null=True)
	update_on = models.DateTimeField(auto_now=True,null=True)

	def __str__(self):
		return self.user.username

class Order(models.Model):
	cust_id = models.ForeignKey(User,on_delete=models.CASCADE)
	cart_ids = models.CharField(max_length=250)
	course_ids = models.CharField(max_length=250)
	invoice_id = models.CharField(max_length=250)
	status = models.BooleanField(default=False)
	processed_on = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.cust_id.username

class Content(models.Model):
	tutor = models.ForeignKey(User,on_delete=models.CASCADE)
	course = models.ForeignKey(add_course,on_delete = models.CASCADE)
	module_no = models.IntegerField(default=1)
	chapter_no = models.IntegerField()
	chapter = models.CharField(max_length=300,null=True,blank=True)
	doc = models.FileField(upload_to="docs/%Y/%m/%d",null=True,blank=True)
	img = models.FileField(upload_to="img/%Y/%m/%d",null=True,blank=True)
	file = models.FileField(upload_to="file/%Y/%m/%d",null=True,blank=True)
	resource = models.FileField(upload_to="resource/%Y/%m/%d",null=True,blank=True)
	added_on = models.DateTimeField(auto_now_add=True,null=True)
	update_on = models.DateTimeField(auto_now=True,null=True)

	def __str__(self):
		return self.tutor.username
