from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.utils import timezone
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import *
from .forms import *

# Create your views here.

def category_list(request):
    categories = Category.objects.all()

    return render(request, 'blog/category_list.html', {'categories':categories})


def category_create(request):
    if request.method =='POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            category = Category(**form.cleaned_data)
            category.save()
            messages.info(request, '새 분류가 등록되었습니다.')
            return redirect('blog:category_list')
    else:
        form = CategoryForm()
    
    return render(request, 'blog/category_form.html', {'form': form})


def post_list(request, category_slug=None):
    category = None
    categories = Category.objects.all()

    posts = Post.objects.all()
    posts = posts.order_by('created')

    # 검색 조건이 있으면 제목에서 해당 내용을 찾는다.
    q = request.GET.get('q', '')
    if q:
        posts = posts.filter(title__icontains=q)

    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        posts = posts.filter(category=category)

    paginator = Paginator(posts, 10)

    page = request.GET.get('page')
    posts = paginator.get_page(page)

    return render(request, 'blog/post_list.html', {'category':category, 'categories':categories, 'posts':posts})


def post_detail(request, slug, id):
    post = get_object_or_404(Post, slug=slug, id=id)

    def get_previous_post(self):
        return self.get_previous_by_updated()

    def get_next_post(self):
        return self.get_next_by_updated()

    return render(request, 'blog/post_detail.html', {'post': post})

@login_required
def post_create(request):
    # POST 요청에 의해 서버로 입력 값을 전송하기 전에 검증
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)
        # 입력 값 검증
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.created = timezone.now()
            post.ip = request.META['REMOTE_ADDR']
            print(form.cleaned_data)
            post = Post(**form.cleaned_data)
            post.save()
            # post.save_tags()
            messages.info(request, '새 글이 등록되었습니다.')
            return redirect('blog:post_detail', post.slug, post.id)
        else:
            form.errors
    else:
        # 글을 새로 생성하려면 폼을 띄워주고(GET), 입력 값 검증에 문제 발생시 form.error에 오류 정보를 저장.
        form = PostForm()
    return render(request, 'blog/post_form.html', {'form': form})

@login_required
def post_edit(request, slug, id):
    post = get_object_or_404(Post, slug=slug, id=id)
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES, instance=Post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.updated = timezone.now()
            post.save()
            return redirect('blog:post_detail', post.slug, post.id)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_form.html', {'form': form})


@login_required
def comment_create(request, slug, id):
    post = get_object_or_404(Post, slug=slug, id=id)
    if request.method == 'POST':
        form = CommentForm(request.POST, request.FILES)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.ip = request.META['REMOTE_ADDR']
            #comment = Comment(**form.cleaned_data)
            comment.save()
            messages.info(request, '새 글이 등록되었습니다.')
            return redirect('blog:post_detail', post.slug, post.id)
        else:
            form.errors()
    else:
        form = CommentForm()
    return render(request, 'blog/comment_form.html', {'form': form})

@login_required
def comment_edit(request, slug, id, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    if comment.author != request.user:
        #return redirect('blog:post_detail', slug, id)
        return redirect(comment.post)

    if request.method == 'POST':
        form = CommentForm(request.POST, request.FILES, instance=comment)
        if form.is_valid():
            comment = form.save()
            return redirect(comment.post)
    else:
        form = CommentForm(instance=comment)
    return render(request, 'blog/comment_form.html', {'form':form,})

@login_required
def comment_delete(request, slug, id, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    if comment.author != request.user:
        return redirect(comment.post)

    if request.method == "POST":
        comment.delete()
        return redirect(comment.post)

    return render(request, 'blog/comment_confirm_delete.html', {'comment':comment,})

