from django import forms
from .models import Product, Category

class AddProductForm(forms.Form):
    category_choice= Category.objects.all()
    category = forms.ChoiceField(coices=category_choice)
    name = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    image = forms.FileInput(upload_to='products/%Y/%m/%d/')
    description = forms.Textarea()
    price = forms.NumberInput()