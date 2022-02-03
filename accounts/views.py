from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views import View
from django.views.generic.edit import UpdateView
from django.views.generic import DetailView
from django.urls import reverse
from django.http import JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin
import os

from django.contrib import messages
from .models import User, Relation, ProfilePhoto
from posts.models import Post
from .forms import UserLoginForm, UserRegistrationForm, ProfileShowPhoto



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
	if request.user is not None :
		
		relation = Relation.objects.filter(from_user=request.user, to_user=user)
		if relation.exists():
			is_following = True
	if request.user.id == user_id:
			self_dash = True
	return render(request, 'accounts/dashboard.html', {'user':user, 'posts':posts, 'self_dash':self_dash, 'is_following':is_following})


class ProfileUpdate(UpdateView):
	model = User
	fields = ('full_name', 'bio', 'age', 'status')
	template_name = 'accounts/update_profile.html'
	
	def get_success_url(self):
           pk = self.kwargs["pk"]
           return reverse("accounts:dashboard", kwargs={"user_id": pk})


@login_required
def follow(request):
	if request.method == 'POST':
		user_id = request.POST['user_id']
		following = get_object_or_404(User, pk=user_id)
		check_relation = Relation.objects.filter(from_user=request.user, to_user=following)
		if check_relation.exists():
			return JsonResponse({'status':'exists'})			
		else:
			Relation(from_user=request.user, to_user=following).save()
			return JsonResponse({'status':'ok'})
			


@login_required
def unfollow(request):
	if request.method == 'POST':
		user_id = request.POST['user_id']
		following = get_object_or_404(User, pk=user_id)
		check_relation = Relation.objects.filter(from_user=request.user, to_user=following)
		if check_relation.exists():
			check_relation.delete()
			return JsonResponse({'status':'ok'})
		else:
			return JsonResponse({'status':'notexists'})

def  show_photo(request, pk):
	user = get_object_or_404(User, pk= pk)
	profile_photos=ProfilePhoto.objects.filter(user=user)
	print ('*'*50)
	print (profile_photos)
	if request.method == 'POST':
		form = ProfileShowPhoto(request.POST,request.FILES)
		if form.is_valid():
			# image_path = user.image.path
			# if os.path.exists(image_path):
			# 	os.remove(image_path)
			
			pfm=form.save(commit=False)
			pfm.user=user
			pfm.save()
			profile_photo=ProfilePhoto.objects.filter(user=user).last()
			user.image=profile_photo.image
			user.save()
			messages.success(request, 'your image updated successfully', 'info')

		return redirect('accounts:show_photo', user.id)
	form = ProfileShowPhoto()
	return render(request,'accounts/show_photo.html', {'user': user, 'form': form, 'profile_photos': profile_photos} )
