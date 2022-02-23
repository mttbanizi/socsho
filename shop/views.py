from django.urls import reverse_lazy
from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils.text import slugify

# project models and forms
from cart.forms import CartAddForm
from .forms import AddProductForm, AddProductCommentForm, AddReplyProductForm, AddProductPhotoForm
from accounts.models import User
from .models import  ProdComment, ProdVote, Category, Product, ProductPhoto



def shop_home(request, category_slug=None):
	products = Product.objects.filter(is_active=True)
	category = get_object_or_404(Category, slug=category_slug)
	if category_slug:
		products = Product.objects.filter(
       		 category__in=Category.objects.get(slug=category_slug).get_descendants(include_self=True)
    		)
	return render(request, 'shop/shop_home.html', {'products': products, 'category': category})

def category_list(request, category_slug=None):
    category = get_object_or_404(Category, slug=category_slug)
    products = Product.objects.filter(
        category__in=Category.objects.get(slug=category_slug).get_descendants(include_self=True)
    )
    return render(request, "shop/category.html", {"category": category, "products": products})


def product_detail(request, slug):
	product = get_object_or_404(Product, slug=slug)
	comments = ProdComment.objects.filter(product=product, is_reply=False)
	form_cart = CartAddForm()
	images=ProductPhoto.objects.filter(product=product)
	can_like = False
	self_dash = False
	if request.user == product.user :
		self_dash= True
	if request.user.is_authenticated:
		if product.user_can_like(request.user):
			can_like = True
	if request.method == 'POST':
		form = AddProductCommentForm(request.POST)
		if form.is_valid():
			new_comment = form.save(commit=False)
			new_comment.product = product
			new_comment.user = request.user
			new_comment.save()
			messages.success(request, 'you comment submitted successfully')
	else:
		form = AddProductCommentForm()
	reply_form=AddReplyProductForm()
	return render(request, 'shop/product_detail.html', {'product': product,'reply_form': reply_form, 'form_cart': form_cart, 'comments': comments, 'form': form, 'can_like': can_like, 'images': images, 'self_dash': self_dash})


class AddProduct(LoginRequiredMixin, View):
	template_name = 'shop/add_product.html'
	form_class = AddProductForm

	def get(self, request, user_id):
		user = get_object_or_404(User, pk=user_id)
		product_image_form = AddProductPhotoForm()
		messages.success(request, user_id)
		return render(request, self.template_name, {'user': user, 'form': self.form_class, 'product_image_form':product_image_form})

	def post(self, request, *args, **kwargs):
		form = self.form_class(request.POST)
		product_image_form = AddProductPhotoForm(request.POST, request.FILES)
		images = request.FILES.getlist('images')
		if form.is_valid():
			new_product=form.save(commit=False)
			new_product.user=request.user
			new_product.slug = slugify(form.cleaned_data['description'][:30])
			
			new_product.save()
			new_product.category.add(form.cleaned_data['category'])
			if images:
				for image in images:
					photo = ProductPhoto.objects.create(image=image,product=new_product)
					messages.success(request, 'your image updated successfully', 'info')
					photo.save()
				new_product.image=photo.image
				new_product.save()
			return redirect('home:all_home')
		return  redirect('home:all_home' )

def product_reply(request, product_id, comment_id):
	product = get_object_or_404(Product, id=product_id)
	comment = get_object_or_404(ProdComment, pk=comment_id)
	if request.method == 'POST':
		form = AddReplyProductForm(request.POST)
		if form.is_valid():
			reply = form.save(commit=False)
			reply.user = request.user
			reply.product = product
			reply.reply = comment
			reply.is_reply = True
			reply.save()
			messages.success(request, 'your reply submitted successfully', 'success')
	return redirect('shop:product_detail',  product.slug)


@login_required
def product_like(request, product_id):
	product = get_object_or_404(Product, id=product_id)
	like = ProdVote(product=product, user=request.user)
	like.save()
	messages.success(request, 'you liked successfully', 'success')
	return redirect('shop:product_detail', product.slug)

def product_dislike(request, product_id):
	product = get_object_or_404(Product, id=product_id)
	dislike = ProdVote.objects.filter(product=product, user=request.user).last().delete()
	messages.success(request, 'you disliked successfully', 'warning')
	return redirect('shop:product_detail', product.slug)

def manage_products(request, user_id):
	user = get_object_or_404(User, pk=user_id)
	products= Product.objects.filter(user=user)
	if request.method== 'POST':
		pass
	return render(request, 'shop/manage_product.html',{'user': user,'products': products })

class ProductDeleteView(DeleteView):
	model = Product
	success_url = reverse_lazy('home:all_home')


class ProductUpdateView(UpdateView):
	model= Product
	fields = ['name', 'description', 'price', 'available']