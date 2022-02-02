from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils.text import slugify
# project models and forms
from cart.forms import CartAddForm
from .forms import AddProductForm, AddProductCommentForm, AddReplyProductForm
from accounts.models import User
from .models import  ProdComment, ProdVote, Category, Product



def shop_home(request, slug=None):
	products = Product.objects.filter(available=True)
	categories = Category.objects.filter(is_sub=False)
	if slug:
		category = get_object_or_404(Category, slug=slug)
		products = products.filter(category=category)
	return render(request, 'shop/shop_home.html', {'products': products, 'categories': categories})


def product_detail(request, slug):
	product = get_object_or_404(Product, slug=slug)
	comments = ProdComment.objects.filter(product=product, is_reply=False)
	form_cart = CartAddForm()
	can_like = False
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
	return render(request, 'shop/product_detail.html', {'product': product,'reply_form': reply_form, 'form_cart': form_cart, 'comments': comments, 'form': form, 'can_like': can_like})


class AddProduct(LoginRequiredMixin, View):
	template_name = 'shop/add_product.html'
	form_class = AddProductForm

	def get(self, request, user_id):
		user = get_object_or_404(User, pk=user_id)
		messages.success(request, user_id)
		return render(request, self.template_name, {'user': user, 'form': self.form_class})

	def post(self, request, *args, **kwargs):
		form = self.form_class(request.POST, request.FILES)
		if form.is_valid():
			new_product=form.save(commit=False)
			new_product.user=request.user
			new_product.slug = slugify(form.cleaned_data['description'][:30])
			new_product.save()
			messages.success(request, 'your image updated successfully', 'info')
			return redirect('shop:home')
		return  redirect('shop:home' )

def add_reply(request, post_id, comment_id):
	product = get_object_or_404(Product, id=post_id)
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
	return redirect('posts:product_detail', product.created.year, product.created.month, product.created.day, product.slug)


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
