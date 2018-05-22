from django import forms
from .models import *



class CategoryForm(forms.ModelForm):

    class Meta:
        model = Category
        fields = ['name']


class PostForm(forms.ModelForm):
    # category = forms.ChoiceField(widget=forms.Select(attrs={'class':'form-control'}))
    # title = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    # title = forms.CharField(widget=forms.TextInput(validators=[min_length_3_validator]))
    # content = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    # Tags = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    

    class Meta:
        model = Post
        fields = ['category', 'title', 'content']

class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = '__all__'