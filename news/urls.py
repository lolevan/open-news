# -*- coding: UTF-8 -*-
# from django.views.decorators.cache import cache_page
from django.urls import path
from django.contrib.auth import views as auth_views

from .views import *

urlpatterns = [
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='news/password_reset_form.html'),
         name='password_reset'),
    path('password_reset/done/',
         auth_views.PasswordResetDoneView.as_view(template_name='news/password_reset_done.html'),
         name='password_reset_done'),
    path('reset/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(template_name='news/password_reset_confirm.html'),
         name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='news/password_reset_complete.html'),
         name='password_reset_complete'),
    path('register/', register, name='register'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
    path('contact/', contact, name='contact'),
    path('', HomeNews.as_view(), name='home'),
    path('category/<int:category_id>/', NewsByCategory.as_view(), name='category'),
    path('news/<int:news_id>/rate/', rate_news, name='rate_news'),
    path('news/<int:pk>/', ViewNews.as_view(), name='view_news'),
    path('news/add-news/', CreateNews.as_view(), name='add_news'),
    path('profile/', ViewProfile.as_view(), name='profile'),
    path('profile/update-news/<int:pk>/', UpdateNewsView.as_view(), name='update_news'),
    path('profile/delete-news/<int:pk>/', DeleteNewsView.as_view()),
]
