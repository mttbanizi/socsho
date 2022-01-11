from django import forms
from .models import Product, Category

class AddProductForm(forms.Form):
    category_choice= Category.objects.all()
    category = forms.ModelChoiceField(queryset=category_choice, widget=forms.Select(attrs={'class': 'form-control'}))
    name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    slug = forms.SlugField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    image = forms.ImageField()

    class Meta:
        model = Product
        fields = ('description', 'price')

