from django.db import models
from django.urls import reverse
from accounts.models import User



class Category(models.Model): # categories
	sub_category = models.ForeignKey('self', on_delete=models.CASCADE, related_name='scategory', null=True, blank=True)
	is_sub = models.BooleanField(default=False)
	name = models.CharField(max_length=200)
	slug = models.SlugField(max_length=200, unique=True)

	class Meta:
		ordering = ('name',)
		verbose_name = 'category'
		verbose_name_plural = 'categories'

	def __str__(self):
		return self.name

	def get_absolute_url(self):
		return reverse('shop:category_filter', args=[self.slug,])



class Product(models.Model):


	user = models.ForeignKey(User, on_delete=models.CASCADE, default="")
	category = models.ManyToManyField(Category, related_name='products')
	name = models.CharField(max_length=200)
	slug = models.SlugField(max_length=200, unique=True)
	image = models.ImageField(upload_to='products/%Y/%m/%d/')
	description = models.TextField(null=True, blank=True)
	price = models.IntegerField(null=True, blank=True)
	available = models.BooleanField(default=True)
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)

	class Meta:
		ordering = ('name',)

	def __str__(self):
		return self.name

	def get_absolute_url(self):
		return reverse('shop:product_detail', args=[self.slug,])

	def likes_count(self):
		return self.prodvote.count()

	def user_can_like(self, user):
		user_like = user.produservote.all()
		qs = user_like.filter(product=self)
		if qs.exists():
			return True
		return False

class ProdComment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='uProdComment')
    product=models.ForeignKey(Product, on_delete=models.CASCADE, null=True, blank=True, related_name='PrProdComment')
    reply = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='rProdComment')
    is_reply = models.BooleanField(default=False)
    body = models.TextField(max_length=400)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user} - {self.body[:30]}'

    class Meta:
        ordering = ('-created',)


class ProdVote(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='prodvote')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='produservote')

    def __str__(self):
        return f'{self.user} liked {self.post}'