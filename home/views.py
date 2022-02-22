from django.shortcuts import render, get_object_or_404

from posts.models import Post
from shop.models import Product, Category

def all_home(request, category_slug=None):
	posts = Post.objects.all()
	products = Product.objects.filter(is_active=True)
	category = Category.objects.filter(name=category_slug)
	if category_slug:
		products = Product.objects.filter(
       		 category__in=Category.objects.get(name=category_slug).get_descendants(include_self=True)
    		)
	return render(request, 'home/all_home.html', {'products': products, 'category': category,'posts': posts})
