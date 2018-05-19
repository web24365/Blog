from django.conf.urls import url
from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    path(r'', views.post_list, name='post_list'),
    path(r'category/', views.category_list, name='category_list'),
    path(r'category/create/', views.category_create, name='category_create'),
    path(r'<slug>/<int:id>/', views.post_detail, name='post_detail'),
    path(r'create/', views.post_create, name='post_create'),
    path(r'<slug>/<int:id>/edit/', views.post_edit, name='post_edit'),
    path(r'<category_slug>/', views.post_list, name='post_list_by_category'),
]

