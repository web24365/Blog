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

    category = forms.ModelChoiceField(queryset=Category.objects.all().order_by('name'), widget=forms.Select(attrs={
        'class':'btn dropdown-toggle bs-placeholder select-with-transition', 
        'data-toggle':'dropdown',
        'role': 'button',}))
        
    title = forms.CharField(label='제목', help_text='제목을 적어주세요', widget=forms.TextInput(attrs={
        'class':'form-control',
    }))
    content = forms.CharField(label='내용', help_text='100 characters max.', widget=forms.Textarea(attrs={
        'class': 'form-control',        
        'rows': 5,
        'cols': 50,
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