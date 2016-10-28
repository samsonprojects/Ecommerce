import os

from mimetypes import guess_type

from django.conf import settings
from django.core.servers.basehttp import FileWrapper
from django.core.files import File
from django.core.urlresolvers import reverse

from django.db.models import Q
from django.http import Http404, HttpResponse
from django.shortcuts import render, get_object_or_404
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.list import ListView

from .models import Product
from .forms import ProductAddForm, ProductModelForm
from .mixins import ProductManagerMixin

from digitalmarket.mixins import (
		MultiSlugMixin,
		SubmitBtnMixin,
		LoginRequiredMixin)


class ProductCreateView(LoginRequiredMixin, SubmitBtnMixin, CreateView):

	model = Product
	template_name = "form.html"
	form_class = ProductModelForm
	# success_url = "/products/"
	submit_btn = "Add Product"

	def form_valid(self, form):
		user = self.request.user
		form.instance.user = user
		valid_data = super(ProductCreateView, self).form_valid(form)
		form.instance.managers.add(user)

		return valid_data

	# def get_success_url(self):
	# 	return reverse("product_list_view")
		

class ProductUpdateView(ProductManagerMixin, SubmitBtnMixin, MultiSlugMixin, UpdateView):
	model = Product
	template_name = "form.html"
	form_class = ProductModelForm
	# success_url = "/products/"
	submit_btn = "Update Product"


class ProductDownloadView(MultiSlugMixin, DetailView):
	model = Product

	def get(self, request, *args, **kwargs):
			obj = self.get_object()
			if obj in request.user.myproducts.products.all():
				filepath = os.path.join(settings.PROTECTED_ROOT, obj.media.path)
				guessed_type = guess_type(filepath)[0]
				filename = open(filepath, 'rb')
				mimetype = 'application/force-download'

				if guessed_type:
					mimetype = guessed_type
				response = HttpResponse(filename, content_type=mimetype)

				if not request.GET.get("preview"):
					response["Content-Disposition"] = "attachment; filename=%s" % (obj.media.name)
				response["X-SendFile"] = str(obj.media.name)	#related to different types of servers
				return response
			else:
				raise Http404


class ProductDetailView(MultiSlugMixin, DetailView):
	model = Product


class ProductListView(ListView):
	model = Product

	def get_queryset(self, *args, **kwargs):
		qs = super(ProductListView, self).get_queryset(**kwargs)
		query = self.request.GET.get("q")
		if query:
			q = qs.filter(
				Q(title__icontains=query)|
				Q(description__icontains=query)
			).order_by("title")
			# qs = qs.filter(title__icontains=query)
			# print(qs)
		return qs


# Create your views here.
def create_view(request):
	form = ProductModelForm(request.POST or None) #create instance by adding ()
	if form.is_valid():
		instance = form.save(commit=False)
		instance.sale_price = instance.price
		instance.save()
		# form.save()

	template = "form.html"
	context = {
		"form": form,
		"submit_btn":"submit button",

	}
	return render(request, template, context)


def update_view(request, object_id=None):
	"""the queryset below will check object has an id , if not raise 404 error"""
	product = get_object_or_404(Product, id=object_id)
	form = ProductModelForm(request.POST or None, instance=product)
	if form.is_valid():
		instance = form.save(commit=False)
		instance.save()

	template = "form.html"
	context = {
		"object": product,
		"form": form,
		"submit_btn": "Update Product",
	}
	return render(request, template, context)



def detail_slug_view(request,slug=None):
	"""the queryset below will check object has an id , if not raise 404 error"""

	try:
		product = get_object_or_404(Product, slug=slug)
	except Product.MultipleObjectsReturned:
		product = Product.objects.filter(slug=slug).order_by("-title").first()	#filter all products with a slug and order by title

	template = "detail_view.html"
	context = {
		"object": product,
	}
	return render(request, template, context)


def detail_view(request,object_id=None):
	"""the queryset below will check object has an id , if not raise 404 error"""
	product = get_object_or_404(Product, id=object_id)
	template = "detail_view.html"
	context = {
		"object": product,
	}
	return render(request, template, context)


def list_view(request):
	print(request)
	template = "list_view.html"
	queryset = Product.objects.all()
	context = {
		"queryset": queryset,
	}
	return render(request, template, context)



