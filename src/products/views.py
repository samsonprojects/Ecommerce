from django.http import Http404
from django.shortcuts import render, get_object_or_404
from .models import Product
from .forms import ProductAddForm, ProductModelForm


# Create your views here.
def create_view(request):
	#FORM
	# print(request.POST)
	form = ProductModelForm(request.POST or None) #create instance by adding ()
	if form.is_valid():
		instance = form.save(commit=False)
		instance.sale_price = instance.price
		instance.save()
		# form.save()

	template = "create_view.html"
	context = {
		"form":form,

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
