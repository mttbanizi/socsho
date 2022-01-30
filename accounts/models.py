from email.policy import default
from django.db import models


from django.contrib.auth.models import AbstractBaseUser
from .managers import MyUserManager

def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT / user_<id>/<filename>
    return 'user_{0}/{1}'.format(instance.user.id, filename)

class User(AbstractBaseUser):
	email = models.EmailField(max_length=100, unique=True)
	full_name = models.CharField(max_length=100)
	is_admin = models.BooleanField(default=False)
	is_active = models.BooleanField(default=True)
	bio = models.TextField(null=True, blank=True)
	age = models.PositiveSmallIntegerField(null=True, blank=True)
	phone = models.PositiveIntegerField(null=True, blank=True)
	image = models.ImageField(upload_to='user/%Y/%m/%d/', default='profile.jpg' )
	status = models.CharField(max_length=300, null=True, blank=True)
	activity= models.CharField(max_length=100, null=True, blank=True)

	objects = MyUserManager()
	USERNAME_FIELD = 'email'
	REQUIRED_FIELDS = ['full_name']

	def __str__(self):
		return self.email

	def image_path(self):
		return '/user/'+str(self.id)

	def has_perm(self, perm, obj=None):
		return True

	def has_module_perms(self, app_label):
		return True

	@property
	def is_staff(self):
		return self.is_admin

class ProfilePhoto(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='uprofilephoto')
	image = models.ImageField(upload_to='user/%Y/%m/%d/', default='profile.jpg' )
	created = models.DateTimeField(auto_now_add=True)

class Relation(models.Model):
	from_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='follower')
	to_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='following')
	created = models.DateTimeField(auto_now_add=True)

	class Meta:
		ordering = ('-created',)

	def __str__(self):
		return f'{self.from_user} following {self.to_user}'