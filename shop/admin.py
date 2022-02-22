from django.contrib import admin


from django import forms
from mptt.admin import MPTTModelAdmin

from .models import (
    Category,
    Product,
    ProductImage,
    ProductSpecification,
    ProductSpecificationValue,
	ProdComment,
    
)
admin.site.register(Category, MPTTModelAdmin)


class ProductSpecificationInline(admin.TabularInline):
    model = ProductSpecification



class ProductImageInline(admin.TabularInline):
    model = ProductImage


class ProductSpecificationValueInline(admin.TabularInline):
    model = ProductSpecificationValue


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    inlines = [
        ProductSpecificationValueInline,
        ProductImageInline,
    ]







admin.site.register(ProdComment)

# @admin.register(Product)
# class ProductAdmin(admin.ModelAdmin):
# 	list_display = ('user', 'name', 'price', 'available')
# 	list_filter = ('available', 'created')
# 	list_editable = ('price',)
# 	prepopulated_fields = {'slug': ('name',)}
# 	raw_id_fields = ('category',)
# 	actions = ('make_available',)
#
# 	def make_available(self, request, queryset):
# 		rows = queryset.update(available=True)
# 		self.message_user(request, f'{rows} updated')
# 	make_available.short_description = 'make all available'
