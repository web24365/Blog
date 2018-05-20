from django.contrib import admin
from django import forms
from .models import Category, Post, TagModel, Comment

# Register your models here.

class PostForm(forms.ModelForm):
    content = forms.CharField(widget=forms.Textarea)

    class Meta:
        model = Post
        fields = '__all__'


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}

admin.site.register(Category, CategoryAdmin)

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['author', 'title', 'content', 'slug', 'Comments', 'created', 'updated', 'published']
    prepopulated_fields = {'slug': ('title',)}
    form = PostForm


@admin.register(TagModel)
class TagModelAdmin(admin.ModelAdmin):
    list_display = ['name']


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    pass
