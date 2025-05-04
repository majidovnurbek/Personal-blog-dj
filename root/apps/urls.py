from django.urls import path
from .views import (
    LoginView,RegisterView,home,post_detail,create_post,admin_dashboard,edit_post,delete_post)
urlpatterns = [
    path('',home, name='home'),
    path('login/',LoginView.as_view(), name='login'),
    path('register/',RegisterView.as_view(), name='register'),
    path('post/<int:post_id>/', post_detail, name='post_detail'),
    path('post/create',create_post, name='create_post'),
    path('dashboard/', admin_dashboard, name='admin_dashboard'),
    path('post/edit/<int:pk>/', edit_post, name='edit_post'),
    path('post/delete/<int:pk>/', delete_post, name='delete_post'),
    


]