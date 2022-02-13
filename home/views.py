from django.shortcuts import render, get_object_or_404

from posts.models import Post
from shop.models import Product, Category

def all_home(request, slug=None):
	posts = Post.objects.all()
	products = Product.objects.filter(available=True)
	categories = Category.objects.filter(is_sub=False)
	if slug:
		category = get_object_or_404(Category, slug=slug)
		products = products.filter(category=category)
	return render(request, 'home/all_home.html', {'products': products, 'categories': categories,'posts': posts})
