from django.shortcuts import render, get_object_or_404, redirect
from django.utils.text import slugify

from django.contrib import messages
# from django.views import View
from django.contrib.auth.decorators import login_required
# from django.contrib.auth.mixins import LoginRequiredMixin
# import redis
# from django.conf import settings
from shop.models import Product, Category
from .models import Post, Comment, Vote
from .forms import AddPostForm, EditPostForm, AddCommentForm, AddReplyForm


def all_posts(request, slug=None):
	posts = Post.objects.all()
	products = Product.objects.filter(available=True)
	categories = Category.objects.filter(is_sub=False)
	if slug:
		category = get_object_or_404(Category, slug=slug)
		products = Product.objects.filter(category=category)
	return render(request, 'posts/all_posts.html', {'products': products, 'categories': categories,'posts': posts})

# redis_con = redis.Redis(settings.REDIS_HOST, settings.REDIS_PORT, settings.REDIS_DB)

def post_detail(request, year, month, day, post_id):
	post = get_object_or_404(Post, created__year=year, created__month=month, created__day=day, pk=post_id)
	comments = Comment.objects.filter(post=post, is_reply=False)
	reply_form = AddReplyForm()
	# redis_con.hsetnx('post_views', post.id, 0)

	rviews='note' 	#rviews = redis_con.hincrby('post_views', post.id)
	can_like = False
	if request.user.is_authenticated:
		if post.user_can_like(request.user):
			can_like = True
	if request.method == 'POST':
		form = AddCommentForm(request.POST)
		if form.is_valid():
			new_comment = form.save(commit=False)
			new_comment.post = post
			new_comment.user = request.user
			new_comment.save()
			messages.success(request, 'you comment submitted successfully')
	else:
		form = AddCommentForm()
	return render(request, 'posts/post_detail.html', {'post':post, 'comments':comments, 'form':form, 'reply':reply_form, 'can_like':can_like, 'rviews':rviews})


# class AddPost(LoginRequiredMixin, View ):
# 	form_class = AddPostForm
# 	template_name = 'posts/add_post.html'
#
# 	def get(self, request, user_id):
# 		if request.user.id != user_id:
# 			return redirect('posts:all_posts')
# 		form = self.form_class
# 		return render(request, self.template_name, {'form': form})
#
# 	def post(self, request, user_id):
# 		if request.user.id != user_id:
# 			return redirect('posts:all_posts')
# 		if self.form_class.is_valid():
# 			new_post = self.form_class.save(commit=False)
# 			new_post.user = request.user
# 			new_post.slug = slugify(self.form_class.cleaned_data['body'][:30])
# 			new_post.save()
# 			messages.success(request, 'your post submitted', 'success')
# 			return redirect('accounts:dashboard', user_id)




@login_required
def add_post(request, user_id):
	if request.user.id == user_id:
		if request.method == 'POST':
			form = AddPostForm(request.POST, request.FILES)
			if form.is_valid():
				new_post = form.save(commit=False)
				new_post.user = request.user
				new_post.slug = slugify(form.cleaned_data['body'][:30], allow_unicode=True)
				new_post.save()
				messages.success(request, 'your post submitted', 'success')
				return redirect('accounts:dashboard', user_id)
		else:
			form = AddPostForm()
		return render(request, 'posts/add_post.html', {'form':form})
	else:
		return redirect('posts:all_posts')

@login_required
def post_delete(request, user_id, post_id):
	if user_id == request.user.id:
		Post.objects.filter(pk=post_id).delete()
		messages.success(request, 'your post deleted successfully', 'success')
		return redirect('accounts:dashboard', user_id)
	else:
		return redirect('posts:all_posts')

@login_required
def post_edit(request, user_id, post_id):
	if request.user.id == user_id:
		post = get_object_or_404(Post, pk=post_id)
		if request.method == 'POST':
			form = EditPostForm(request.POST, instance=post)
			if form.is_valid():
				ep = form.save(commit=False)
				ep.slug = slugify(form.cleaned_data['body'][:30])
				ep.save()
				messages.success(request, 'your post edited successfully', 'success')
				return redirect('accounts:dashboard', user_id)
		else:
			form = EditPostForm(instance=post)
		return render(request, 'posts/edit_post.html', {'form':form})
	else:
		return redirect('posts:all_posts')


@login_required
def add_reply(request, post_id, comment_id):
	post = get_object_or_404(Post, id=post_id)
	comment = get_object_or_404(Comment, pk=comment_id)
	if request.method == 'POST':
		form = AddReplyForm(request.POST)
		if form.is_valid():
			reply = form.save(commit=False)
			reply.user = request.user
			reply.post = post
			reply.reply = comment
			reply.is_reply = True
			reply.save()
			messages.success(request, 'your reply submitted successfully', 'success')
	return redirect('posts:post_detail', post.created.year, post.created.month, post.created.day, post.id)


@login_required
def post_like(request, post_id):
	post = get_object_or_404(Post, id=post_id)
	like = Vote(post=post, user=request.user)
	like.save()
	messages.success(request, 'you liked successfully', 'success')
	return redirect('posts:post_detail', post.created.year, post.created.month, post.created.day, post.id)


@login_required
def post_dislike(request, post_id):
	post = get_object_or_404(Post, id=post_id)
	dislike = Vote.objects.filter(post=post, user=request.user).delete()
	messages.success(request, 'you disliked successfully', 'warning')
	return redirect('posts:post_detail', post.created.year, post.created.month, post.created.day, post.id)





