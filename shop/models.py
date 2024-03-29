from email.mime import image
from itertools import product
from django.db import models
from django.urls import reverse
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from mptt.models import MPTTModel, TreeForeignKey

from accounts.models import User




class Category(MPTTModel): # categories
	name = models.CharField(
		verbose_name=_("Category Name"), 
		help_text=_("Required and unique"),
		max_length=255,	
		unique=True
		)
	slug = models.SlugField(verbose_name=_("Category safe URL"), max_length=255, unique=True)
	parent = TreeForeignKey("self", on_delete=models.CASCADE, null=True, blank=True, related_name="children")
	is_active = models.BooleanField(default=True)

	class MPTTMeta:
		order_insertion_by = ["name"]

	class Meta:
		verbose_name = _("Category")
		verbose_name_plural = _("Categories")

	def get_absolute_url(self):
		return reverse("home:category_filter", args=[self.slug])

	def __str__(self):
		return self.name

class ProductType(models.Model):
    """
    ProductType Table will provide a list of the different types
    of products that are for sale.
    """

    name = models.CharField(verbose_name=_("Product Name"), help_text=_("Required"), max_length=255, unique=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = _("Product Type")
        verbose_name_plural = _("Product Types")

    def __str__(self):
        return self.name


class ProductSpecification(models.Model):
    """
    The Product Specification Table contains product
    specifiction or features for the product types.
    """

    category = models.ForeignKey(Category, on_delete=models.RESTRICT, related_name='C_product_secification')
    name = models.CharField(verbose_name=_("Name"), help_text=_("Required"), max_length=255)

    class Meta:
        verbose_name = _("Product Specification")
        verbose_name_plural = _("Product Specifications")

    def __str__(self):
        return self.name


class Product(models.Model):
    
	user = models.ForeignKey(User, on_delete=models.CASCADE, default="")
	category = models.ForeignKey(Category, on_delete=models.RESTRICT)
	title = models.CharField(
        verbose_name=_("title"),
        help_text=_("Required"),
        max_length=255,
    )
	description = models.TextField(verbose_name=_("description"), help_text=_("Not Required"), blank=True)
	slug = models.SlugField(max_length=255)
	price = models.DecimalField(
        verbose_name=_("Regular price"),
        help_text=_("Maximum 999.99"),
        error_messages={
            "name": {
                "max_length": _("The price must be between 0 and 999.99."),
            },
        },
        max_digits=5,
        decimal_places=2,
    )
	discount_price = models.DecimalField(
        verbose_name=_("Discount price"),
        help_text=_("Maximum 999.99"),
        error_messages={
            "name": {
                "max_length": _("The price must be between 0 and 999.99."),
            },
        },
        max_digits=5,
        decimal_places=2,
    )
	is_active = models.BooleanField(
        verbose_name=_("Product visibility"),
        help_text=_("Change product visibility"),
        default=True,
    )
	created_at = models.DateTimeField(_("Created at"), auto_now_add=True, editable=False)
	updated_at = models.DateTimeField(_("Updated at"), auto_now=True)
	users_wishlist = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="user_wishlist", blank=True)

	class Meta:
		ordering = ("-created_at",)
		verbose_name = _("Product")
		verbose_name_plural = _("Products")

	def get_absolute_url(self):
		return reverse("shop:product_detail", args=[self.slug])

	def __str__(self):
		return self.title

	def likes_count(self):
		return self.prodvote.count()

	def user_can_like(self, user):
		user_like = user.produservote.all()
		qs = user_like.filter(product=self)
		if qs.exists():
			return True
		return False


class ProductSpecificationValue(models.Model):
    """
    The Product Specification Value table holds each of the
    products individual specification or bespoke features.
    """

    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='P_product_specificatiob_value')
    specification = models.ForeignKey(ProductSpecification, on_delete=models.RESTRICT)
    value = models.CharField(
        verbose_name=_("value"),
        help_text=_("Product specification value (maximum of 255 words"),
        max_length=255,
    )

    class Meta:
        verbose_name = _("Product Specification Value")
        verbose_name_plural = _("Product Specification Values")

    def __str__(self):
        return self.value


class ProductImage(models.Model):
    """
    The Product Image table.
    """

    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="product_image")
    image = models.ImageField(
        verbose_name=_("image"),
        help_text=_("Upload a product image"),
        upload_to="images/",
        default="images/default.png",
    )
    alt_text = models.CharField(
        verbose_name=_("Alturnative text"),
        help_text=_("Please add alturnative text"),
        max_length=255,
        null=True,
        blank=True,
    )
    is_feature = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Product Image")
        verbose_name_plural = _("Product Images")


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
        return f'{self.user} liked {self.product}'


class ProductPhoto(models.Model):
	product=models.ForeignKey(Product,on_delete=models.CASCADE,related_name="p_photo")
	image = models.ImageField(upload_to='products/%Y/%m/%d/')
	created = models.DateTimeField(auto_now_add=True)


class ProducVideo(models.Model):
    """
    The Product Image table.
    """

    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="product_video")
    Video = models.FileField(
        verbose_name=_("Video"),
        help_text=_("Upload a product video"),
        upload_to="video/",
        default="video/default.mp4",
    )
    alt_text = models.CharField(
        verbose_name=_("Alturnative text"),
        help_text=_("Please add alturnative text"),
        max_length=255,
        null=True,
        blank=True,
    )
    created_at = models.DateTimeField(auto_now_add=True, editable=False)

    class Meta:
        verbose_name = _("Product video")
        verbose_name_plural = _("Product video")

