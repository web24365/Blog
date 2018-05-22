from django.conf.urls import url
from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.post_list, name='post_list'),
    path('category/', views.category_list, name='category_list'),
    path('category/create/', views.category_create, name='category_create'),
    path('<category_slug>/', views.post_list, name='post_list_by_category'),
    path('<slug>/<int:id>/', views.post_detail, name='post_detail'),
    path('<slug>/<int:id>/edit/', views.post_edit, name='post_edit'),
    path('create/', views.post_create, name='post_create'),
    path('<slug>/<int:id>/comment/create/', views.comment_create, name='comment_create'),
    path('<slug>/<int:id>/comment/<int:comment_id>/edit/', views.comment_edit, name='comment_edit'),
    path('<slug>/<int:id>/comment/<int:comment_id>/delete/', views.comment_delete, name='comment_delete'),

]

