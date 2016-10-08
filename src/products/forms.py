from django import forms 
from .models import Product

PUBLISH_CHOICES = (
	('publish', "Publish"),
	('draft', "Draft"),
)

class ProductAddForm(forms.Form):
	title = forms.CharField(label='Your Title',widget=forms.TextInput(
		attrs={
		"class":"custom-class",
		"placeholder":"Title",
		}
		))
	description = forms.CharField(widget=forms.Textarea(
		attrs={"class": "my-custom-class",
		"placeholder": "description",
		"some-attr": "this",
		}
	))
	price = forms.DecimalField()
	publish = forms.ChoiceField(widget=forms.RadioSelect, choices=PUBLISH_CHOICES, required=False)

	def clean_price(self):
		"""form validation of fields """
		price = self.cleaned_data.get("price")
		if price <= 1.00:
			raise forms.ValidationError("Price must be grater than $1")
		elif price >= 99.99:
			raise forms.ValidationError("Price must be less than 100")
		else:
			return price

	def clean_title(self):
		title = self.cleaned_data.get("title")
		if len(title) > 3:
			return title
		else:
			raise forms.ValidationError("Title must be longer than 3")


class ProductModelForm(forms.ModelForm):
	publish = forms.ChoiceField(widget=forms.RadioSelect, choices=PUBLISH_CHOICES, required=False)


	class Meta:
		model = Product
		fields = [
		"title",
		"description",
		"price",
		]
		
	def clean_price(self):
		price = self.cleaned_data("price")
		if price <=1.00:
			raise forms.ValidationError("Price must be greater than 1 ")
		elif price >= 99.99:
			raise forms.ValidationError("Price must be below 100")
		else:
			return price
"""
	title = models.CharField(max_length=30) #;lasfdjksdl;aj;lasdjsdaj
	slug = models.SlugField(blank=True) #unique=True
	description = models.TextField()
	price = models.DecimalField(max_digits=100, decimal_places=2, default=9.99)  #100.00
	sale_price = models.DecimalField(max_digits=100, decimal_places=2, default=6.99, null=True, blank=True)  #100.00

"""


