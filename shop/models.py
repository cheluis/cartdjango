from django.contrib.auth.models import User
from django.db import models
import datetime

ORDER_STATUS = (('A', 'ACTIVE'), ('P', 'PROCESSED'), ('D', 'DOWNLOADED'))

# Register your models here.
class PaymentMethod(models.Model):
    name = models.CharField(max_length = 150)
    class Meta:
        verbose_name = "PaymentMethod"
        verbose_name_plural = "PaymentMethods"

    def __unicode__(self):
    	return self.name

class Category(models.Model):
	name = models.CharField(max_length = 150)
	class Meta:
		verbose_name = "Category"
		verbose_name_plural = "Categories"
	def __unicode__(self):
		return self.name


class PublicationType(models.Model):
	name = models.CharField(max_length = 15)
	downloadable = models.BooleanField(default = False)

	class Meta:
		verbose_name = "Publication Type"
		verbose_name_plural = "Publication Types"
	def __unicode__(self):
		return self.name

class Publication(models.Model):
	name = models.CharField(max_length = 255)
	date_published = models.DateField()
	publication_types = models.ManyToManyField(PublicationType)
	categories = models.ManyToManyField(Category)
	author = models.CharField(max_length = 255)
	price = models.DecimalField(default = 0, null = True, blank = True, max_digits = 10, decimal_places = 2)
	thumbnail = models.ImageField(upload_to = 'thumbnails', default = '')
	pdf_file = models.FileField(null = True, blank = True) 
	audio_file = models.FileField(null = True, blank = True)
	
	class Meta:
		verbose_name = "Publication"
		verbose_name_plural = "Publications"

	def __unicode__(self):
		return self.name

class Order(models.Model):
	user = models.ForeignKey(User)
	order_date = models.DateField(auto_now = True)
	order_status = models.CharField(max_length = 1, choices = ORDER_STATUS, default = 'A')
	order_address = models.TextField(null = True, blank = True)
	order_payment_method = models.ForeignKey(PaymentMethod, null = True)
	order_payment_number = models.CharField(max_length = 20, null = True, blank = True)
	class Meta:
		verbose_name = "Order"
		verbose_name_plural = "Orders"
	
	def __unicode__(self):
		return self.user.username
    
class OrderDetail(models.Model):
	order = models.ForeignKey(Order)
	order_item = models.ForeignKey(Publication)
	order_quantity = models.IntegerField()
	order_presentation = models.ForeignKey(PublicationType, null = True, blank = True)    