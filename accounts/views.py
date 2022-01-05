from django.shortcuts import render, redirect, get_object_or_404
from .forms import UserLoginForm, UserRegistrationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from django.contrib import messages
from .models import User, Relation
from posts.models import Post


def user_login(request):
	if request.method == 'POST':
		form = UserLoginForm(request.POST)
		if form.is_valid():
			cd = form.cleaned_data
			user = authenticate(request, email=cd['email'], password=cd['password'])
			if user is not None:
				login(request, user)
				messages.success(request, 'you logged in successfully', 'success')
				return redirect('accounts:dashboard', user.id)
			else:
				messages.error(request, 'username or password is wrong', 'danger')
	else:
		form = UserLoginForm()
	return render(request, 'accounts/login.html', {'form':form})


def user_logout(request):
	logout(request)
	messages.success(request, 'you logged out successfully', 'success')
	return redirect('accounts:login')


def user_register(request):
	if request.method == 'POST':
		form = UserRegistrationForm(request.POST)
		if form.is_valid():
			cd = form.cleaned_data
			user = User.objects.create_user(cd['email'], cd['full_name'], cd['password'])
			user.save()
			messages.success(request, 'you registered successfully', 'success')
			return redirect('accounts:dashboard', user.id)
	else:
		form = UserRegistrationForm()
	return render(request, 'accounts/register.html', {'form':form})



def user_dashboard(request, user_id):
	user = get_object_or_404(User, pk=user_id)
	posts = Post.objects.filter(user=user)
	self_dash = False
	is_following = False
	print('******************************************************')
	print (user_id)
	relation = Relation.objects.filter(from_user=request.user, to_user=user)
	if relation.exists():
		is_following = True
	if request.user.id == user_id:
		self_dash = True
	return render(request, 'accounts/dashboard.html', {'user':user, 'posts':posts, 'self_dash':self_dash, 'is_following':is_following})

