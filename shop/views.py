from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages

from .models import Category, Product
from cart.forms import CartAddForm
from .forms import AddProductForm
from accounts.models import User



def shop_home(request, slug=None):
	products = Product.objects.filter(available=True)
	categories = Category.objects.filter(is_sub=False)
	if slug:
		category = get_object_or_404(Category, slug=slug)
		products = products.filter(category=category)
	return render(request, 'shop/shop_home.html', {'products': products, 'categories': categories})


def product_detail(request, slug):
	product = get_object_or_404(Product, slug=slug)
	form = CartAddForm()
	return render(request, 'shop/product_detail.html', {'product': product, 'form': form})


def add_product(request):
	form= AddProductForm()
	return render(request, 'shop/add_product.html', { 'form': form})


class AddProduct(LoginRequiredMixin, View):
	template_name = 'shop/add_product.html'
	form_class = AddProductForm

	def get(self, request, username):
		user = get_object_or_404(User, username=username)
		return render(request, self.template_name, {'user': user, 'form': self.form_class})

	def post(self, request, *args, **kwargs):
		form = self.form_class(request.POST, request.FILES)
		if form.is_valid():
			form.save()
			messages.success(request, 'your image updated successfully', 'info')
			return redirect('shop:shop', request.user.username)