from django.conf import settings

from django.db import models
from django.db.models.signals import pre_save, post_save
from django.utils.text import slugify

# Create your models here.


class Product(models.Model):
	user = models.ForeignKey(settings.AUTH_USER_MODEL)
	managers = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="managers_product", blank=True)
	title = models.CharField(max_length=30) #;lasfdjksdl;aj;lasdjsdaj
	slug = models.SlugField(blank=True, unique=True) 
	description = models.TextField()
	price = models.DecimalField(max_digits=100, decimal_places=2, default=9.99)  #100.00
	sale_price = models.DecimalField(max_digits=100, decimal_places=2, default=6.99, null=True, blank=True)  #100.00

	def __str__(self):
		return self.title


def create_slug(instance, new_slug=None):
	slug = slugify(instance.title)
	if new_slug is not None:
		slug = new_slug

	qs = Product.objects.filter(slug=slug)
	exists = qs.exists()
	if qs:
		new_slug = "%s-%s" % (slug, qs.first().id)
		return create_slug(instance, new_slug=new_slug)
	return slug


def product_pre_save_reciever(sender, instance, *args, **kwargs): #with args and kwargs any additional keyword arguments wont cause an error
	"""makes sure the product is slugifyed before the instance is saved on the database """
	if not instance.slug:
		instance.slug = create_slug(instance)

pre_save.connect(product_pre_save_reciever,sender=Product)


# def product_post_save_reciever(sender, instance, *args, **kwargs): #with args and kwargs any additional keyword arguments wont cause an error
""""""

# 	if instance.slug != slugify(instance.title):
# 		instance.slug = slugify(instance.title)
# 		instance.save()

# pre_save.connect(product_pre_save_reciever,sender=Product)