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
    # def __init__(self, *args, **kwargs):
    #     super(PostForm, self).__init__(*args, **kwargs)
    #     self.fields['category'].widget.choices = Category.objects.all()

    category = forms.ModelMultipleChoiceField(queryset=Category.objects.all().order_by('name'), widget=forms.Select(attrs={'class':'form-contrl',}))
        
    title = forms.CharField(label='제목', widget=forms.TextInput(attrs={
        'class':'form-control',
        'help_text': '',
    }))
    content = forms.CharField(label='내용', widget=forms.Textarea(attrs={
        'class': 'form-control',
        'help_text': '100 characters max.',
        'rows': 5,
        'cols': 50,
        'help_text': '글',
        'size': '70px',
        'placeholder': '', }))
    
    class Meta:
        model = Post
        fields = ['category', 'title', 'content']

class CommentForm(forms.ModelForm):
    message = forms.CharField(label='', widget=forms.TextInput(attrs={
        'class': 'comment-form',
        'size': '70px',
        'placeholder': '댓글 달기...',
        'maxlength': '40', }))

    class Meta:
        model = Comment
        fields = ['message']