from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views import View
from django.views.generic.edit import UpdateView
from django.views.generic import DetailView
from django.urls import reverse
from django.http import JsonResponse
import os
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy

from django.contrib import messages
from .models import User, Relation, ProfilePhoto
from posts.models import Post
from .forms import UserLoginForm, UserRegistrationForm, ProfileShowPhoto



def user_login(request):
	print (50*'L')
	print (request.user.is_authenticated)
	if request.user.is_authenticated:
		if request.GET.get('next'):
			return redirect(request.GET.get('next'))
		return redirect('accounts:dashboard', request.user.id)
	if request.method == 'POST':
		form = UserLoginForm(request.POST)
		if form.is_valid():
			cd = form.cleaned_data
			user = authenticate(request, email=cd['email'], password=cd['password'])
			if user is not None:
				login(request, user)
				messages.success(request, 'you logged in successfully', 'success')
				if request.GET.get('next'):
					return redirect(request.GET.get('next'))
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

@login_required
def others_dashboard(request, user_id):
	user = get_object_or_404(User, pk=user_id)
	posts = Post.objects.filter(user=user)
	is_following = False
	is_requested= False
	num_follower=Relation.objects.filter(to_user=user, accepted=True).count()
	num_following=Relation.objects.filter(from_user=user, accepted=True).count()
	num_requests=0
	if request.user is not None :
		
		relation = Relation.objects.filter(from_user=request.user, to_user=user).last()
		print (relation) 
		if relation != None :
			print (relation.accepted)
			if relation.accepted :
				is_following = True
			else: 
				is_requested = True
	
	print (is_requested)
	return render(request, 'accounts/dashboard.html', {'user':user, 'posts':posts, 
														'num_requests':num_requests, 'is_requested':is_requested,
														 'is_following':is_following, 'num_follower':	num_follower, 
														 'num_following': num_following })

@login_required
def user_dashboard(request, user_id):
	user = get_object_or_404(User, pk=user_id)
	posts = Post.objects.filter(user=user)
	self_dash = True
	
	print('******************************************************')
	
	num_follower=Relation.objects.filter(to_user=user, accepted=True).count()
	num_following=Relation.objects.filter(from_user=user, accepted=True).count()
	num_requests=0
	
	return render(request, 'accounts/dashboard.html', {'user':user, 'posts':posts, 'self_dash':self_dash, 
													'num_follower':	num_follower,  'num_following': num_following })


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
		if following.private :
			send_request = Relation.objects.create(from_user=request.user, to_user=following, accepted= False)
			send_request.save()
			return JsonResponse({'status':'private'})
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

@login_required
def  show_photo(request, pk):
	user = get_object_or_404(User, pk= pk)
	profile_photos=ProfilePhoto.objects.filter(user=user)
	self_dash= False
	if user == request.user :
		self_dash=True
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
	return render(request,'accounts/show_photo.html', {'self_dash':self_dash, 'user': user, 'form': form, 'profile_photos': profile_photos} )

@login_required
def update_photo(request, user_id, image_id):
	user = get_object_or_404(User, pk= user_id)
	if user == request.user :
		profile_photo=get_object_or_404(ProfilePhoto,pk=image_id)
		user.image=profile_photo.image
		user.save()
	return redirect('accounts:dashboard', user.id)


class UserPasswordResetView(auth_views.PasswordResetView):
	template_name = 'accounts/password_reset_form.html'
	success_url = reverse_lazy('accounts:password_reset_done')
	email_template_name = 'accounts/password_reset_email.html'


class UserPasswordResetDoneView(auth_views.PasswordResetDoneView):
	template_name = 'accounts/password_reset_done.html'


class UserPasswordResetConfirmView(auth_views.PasswordResetConfirmView):
	template_name = 'accounts/password_reset_confirm.html'
	success_url = reverse_lazy('accounts:password_reset_complete')


class UserPasswordResetCompleteView(auth_views.PasswordResetCompleteView):
	template_name = 'accounts/password_reset_complete.html'


class follow_requests(LoginRequiredMixin, View):
	def get(self,request):
		follow_requests=Relation.objects.filter(to_user=request.user, accepted=False)
		
		return render(request,'accounts/requests.html', {'follow_requests': follow_requests,} )

def accept_request(request):
	
		if request.method == 'POST':

			user_id = request.POST['user_id']
			follower = get_object_or_404(User, pk=user_id)
			print (user_id)
			check_relation = Relation.objects.filter(from_user=follower, to_user=request.user).last()
			print(50*'f')
			print (check_relation.from_user)
			if check_relation:
				check_relation.accepted = True
				check_relation.save()
				print("relation exist")
				return JsonResponse({'status':'ok'})
			else:
				return JsonResponse({'status':'notexists'})



class follower_list(LoginRequiredMixin, View):
	def get(self,request):
		followers=Relation.objects.filter(to_user=request.user, accepted=True)
		
		return render(request,'accounts/follower_list.html', {'followers': followers,} )


def reject_follow(request):
	
		if request.method == 'POST':

			user_id = request.POST['user_id']
			follower = get_object_or_404(User, pk=user_id)
			print (user_id)
			check_relation = Relation.objects.filter(from_user=follower, to_user=request.user).last()
			print(50*'f')
			print (check_relation.from_user)
			if check_relation:
				check_relation.delete()
				print("relation deleted")
				return JsonResponse({'status':'ok'})
			else:
				return JsonResponse({'status':'notexists'})


class following_list(LoginRequiredMixin, View):
	def get(self,request):
		followeing=Relation.objects.filter(from_user=request.user)
		print(followeing)
		return render(request,'accounts/followeing_list.html', {'followeing': followeing,} )

def cancel_following(request):
	
		if request.method == 'POST':

			user_id = request.POST['user_id']
			follower = get_object_or_404(User, pk=user_id)
			print (user_id)
			check_relation = Relation.objects.filter(to_user=follower, from_user=request.user).last()
			print(50*'f')
			print (check_relation.from_user)
			if check_relation:
				check_relation.delete()
				print("relation deleted")
				return JsonResponse({'status':'ok'})
			else:
				return JsonResponse({'status':'notexists'})
