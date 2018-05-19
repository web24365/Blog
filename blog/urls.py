from django.conf.urls import url
from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.post_list, name='post_list'),
    path('category/', views.category_list, name='category_list'),
    path('category/create/', views.category_create, name='category_create'),
    path('<slug>/<int:id>/', views.post_detail, name='post_detail'),
    path('create/', views.post_create, name='post_create'),
    path('<slug>/<int:id>/edit/', views.post_edit, name='post_edit'),
    path('<category_slug>/', views.post_list, name='post_list_by_category'),
]

