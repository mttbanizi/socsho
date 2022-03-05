from django.shortcuts import render, get_object_or_404

from posts.models import Post
from shop.models import Product, Category

def all_home(request, category_slug=None):
	posts = Post.objects.all()
	products = Product.objects.all()
	category = Category.objects.filter(slug=category_slug)
	print (50*'&')
	print (products.values())
	if category_slug:
		products = Product.objects.filter(
       		 category__in=Category.objects.get(slug=category_slug).get_descendants(include_self=True)
    		)
	return render(request, 'home/all_home.html', {'products': products, 'category': category,'posts': posts})
