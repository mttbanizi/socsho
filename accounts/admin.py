from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .forms import UserCreationForm, UserChangeForm
from .models import User, Relation, ProfilePhoto
from django.contrib.auth.models import Group


class UserAdmin(BaseUserAdmin):
	form = UserChangeForm
	add_form = UserCreationForm
	list_display = ('full_name', 'email', 'is_admin')
	list_filter = ('is_admin',)
	fieldsets = (
		('Main', {'fields':('full_name', 'email', 'password')}),
		( 'profile',{
			'fields':('age','bio', 'phone', 'status')
		}),
		('Personal info', {'fields':('is_active',)}),
		('Permissions', {'fields':('is_admin','private')})
	)
	add_fieldsets = (
		(None, {
			'fields':('full_name', 'email', 'password1', 'password2')
		}),
		
		( 'profile photo',{
			'fields':('image',)
		})


	)
	search_fields = ('email',)
	ordering = ('email',)
	filter_horizontal = ()


admin.site.register(User, UserAdmin)
admin.site.unregister(Group)
admin.site.register(Relation)
admin.site.register(ProfilePhoto)