from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.db import models
from django.db.models.signals import pre_save, post_save
from django.core.urlresolvers import reverse #reverse takes a url name/view name and makes it more dynamic
from django.utils.text import slugify

# Create your models here.




def download_media_location(instance, filename):
	""" the location is customising where the file will be uploaded to"""
	return "%s/%s" % (instance.slug, filename)

class Product(models.Model):
	user = models.ForeignKey(settings.AUTH_USER_MODEL)
	managers = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="managers_product", blank=True)
	media = models.ImageField(blank=True,
			null=True,
			upload_to=download_media_location,
			storage=FileSystemStorage(location=settings.PROTECTED_ROOT))
	title = models.CharField(max_length=30) #;lasfdjksdl;aj;lasdjsdaj
	slug = models.SlugField(blank=True, unique=True) 
	description = models.TextField()
	price = models.DecimalField(max_digits=100, decimal_places=2, default=9.99)  #100.00
	sale_price = models.DecimalField(max_digits=100, decimal_places=2, default=6.99, null=True, blank=True)  #100.00

	def __str__(self):
		return self.title

	def get_absolute_url(self):
		view_name = "products:detail_slug"
		return reverse(view_name, kwargs={"slug": self.slug})

	def get_download(self):
		view_name = "products:download_slug"
		url = reverse(view_name, kwargs={"slug": self.slug})
		return url
		# return url


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


def product_pre_save_receiver(sender, instance, *args, **kwargs): #with args and kwargs any additional keyword arguments wont cause an error
	"""makes sure the product is slugifyed before the instance is saved on the database """
	if not instance.slug:
		instance.slug = create_slug(instance)

pre_save.connect(product_pre_save_receiver, sender=Product)


class MyProducts(models.Model):
	user = models.OneToOneField(settings.AUTH_USER_MODEL)
	products = models.ManyToManyField(Product, blank=True)

	def __str__(self):
		""" gets the products queryset"""
		return "%s" % (self.products.count())

	class Meta:
		verbose_name = "My Product"
		verbose_name_plural = "My Products"


def thumbnail_location(instance, filename):
	""" the location is customising where the file will be uploaded to"""
	return "%s/%s" % (instance.product.slug, filename)

THUMB_CHOICES = (
	("hd", "HD"),
	("sd", "SD"),
	("micro", "Micro"),
)


class Thumbnail(models.Model):
	product = models.ForeignKey(Product)
	type = models.CharField(max_length=20, choices=THUMB_CHOICES, default='hd')
	height = models.CharField(max_length=20, null=True, blank=True)
	width = models.CharField(max_length=20, null=True, blank=True)
	media = models.ImageField(
		width_field = "width",
		height_field = "height",
		blank=True,
		null=True,
		upload_to=thumbnail_location)

	def __str__(self):
		return str(self.media.path)

import os
import shutil
from PIL import Image
import random
from django.core.files import File


def product_post_save_receiver(sender, instance, created, *args, **kwargs):
	"""imag uploaded to this function"""
	if instance.media:
		# create thumbnail instance three types
		hd = Thumbnail.objects.get_or_create(product=instance, type='hd')[0]
		sd = Thumbnail.objects.get_or_create(product=instance, type='hd')[0]
		micro = Thumbnail.objects.get_or_create(product=instance, type='hd')[0]

		hd_max = (400, 400)
		sd_max = (200, 200)
		micro_max = (50, 50)

		print(instance.media.path)
		filename = os.path.basename(instance.media.path)
		thumb = Image.open(instance.media.path) #created thumbnail image 
		thumb.thumbnail(hd_max, Image.ANTIALIAS)

		temp_loc = "%s/%s/tmp" %(settings.MEDIA_ROOT, instance.slug) #created a temp location for all images
		
		if not os.path.exists(temp_loc):
			os.makedirs(temp_loc)

		temp_file_path = os.path.join(temp_loc, filename) # created filepath with file name in there
		if os.path.exists(temp_file_path): #if image already exists create another or more random one
			temp_file_path = os.path.join(temp_loc, "%s" %(random.random()))
			os.makedirs(temp_path)
			temp_file_path = os.path.join(temp_path, filename)

		temp_image = open(temp_file_path, "w")
		thumb.save(temp_image)
		thumb_data = open(temp_file_path, "r")

		thumb_file = File(thumb_data)
		hd.media.save(file, thum_file)
		# shutil.rmtree(tem_loc, ignore_errors=True)

post_save.connect(product_post_save_receiver, sender=Product)










