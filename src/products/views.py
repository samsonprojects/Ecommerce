
from django.http import Http404
from django.shortcuts import render, get_object_or_404
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.list import ListView

from .models import Product
from .forms import ProductAddForm, ProductModelForm
from digitalmarket.mixins import MultiSlugMixin, SubmitBtnMixin


class ProductCreateView(SubmitBtnMixin, CreateView):

	model = Product
	template_name = "form.html"
	form_class = ProductModelForm
	success_url = "/products/add"
	submit_btn = "Add Product"


class ProductUpdateView(SubmitBtnMixin, MultiSlugMixin, UpdateView):
	model = Product
	template_name = "form.html"
	form_class = ProductModelForm
	success_url = "/products/"
	submit_btn = "Update Product"

	def get_object(self, *args, **kwargs):
		"""it looks to see if user in managers and check if user is authenticated"""
		user = self.request.user
		obj = super(ProductUpdateView, self).get_object(*args, **kwargs) #superclass of current view
		if obj.user == user or user in obj.managers.all():
			return obj
		else:
			raise Http404


class ProductDetailView(MultiSlugMixin, DetailView):
	model = Product


class ProductListView(ListView):
	model = Product

	def get_queryset(self, *args, **kwargs):
		qs = super(ProductListView, self).get_queryset(**kwargs)
		# qs = qs.filter(title__icontains="aaaaaaa")
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
		"form":form,
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



