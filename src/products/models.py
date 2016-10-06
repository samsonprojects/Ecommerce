from django.db import models
from django.db.models.signals import pre_save
# Create your models here.


class Product(models.Model):
	title = models.CharField(max_length=30) #;lasfdjksdl;aj;lasdjsdaj
	slug = models.SlugField(default='slug-field') #unique=True
	description = models.TextField()
	price = models.DecimalField(max_digits=100, decimal_places=2, default=9.99)  #100.00
	sale_price = models.DecimalField(max_digits=100, decimal_places=2, default=6.99, null=True, blank=True)  #100.00

	def __str__(self):
		return self.title


	def product_pre_save_reciever(sender, instance, *args, **kwargs):
		print(sender)
		print(instance)