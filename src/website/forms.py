from django import forms
from .models import Product, Category, Rate, Comment, ProductPicture


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = '__all__'


class RateForm(forms.ModelForm):
    class Meta:
        model = Rate
        fields = '__all__'


class ProductPictureForm(forms.ModelForm):
    class Meta:
        model = ProductPicture
        fields = '__all__'


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Add your comment here...'}),
        }


class ProductSearchForm(forms.Form):
    query = forms.CharField(
        label='Search Products',
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Search...'})
    )
