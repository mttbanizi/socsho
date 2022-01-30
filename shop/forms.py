from django import forms
from .models import Product, Category, ProdComment

class AddProductForm(forms.ModelForm):
    category_choice= Category.objects.all()
    category = forms.ModelChoiceField(queryset=category_choice, widget=forms.Select(attrs={'class': 'form-control'}))
    name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'size':30}))
    image = forms.ImageField()

    class Meta:
        model = Product
        fields = ('image',  'name' , 'category', 'description', 'price')


class AddProductCommentForm(forms.ModelForm):
	class Meta:
		model = ProdComment
		fields = ('body',)
		widgets = {
			'body': forms.Textarea(attrs={'class':'form-control'})
		}
		error_messages = {
			'body': {
				'required': 'این فیلد اجباری است',
			}
		}
		help_texts = {
			'body': 'max 400 char'
		}

class AddReplyProductForm(forms.ModelForm):
		class Meta:
			model = ProdComment
			fields = ('body',)