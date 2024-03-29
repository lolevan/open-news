# -*- coding: UTF-8 -*-
# from django.views.decorators.cache import cache_page
from django.urls import path

from .views import *

urlpatterns = [
    # path('', index, name='home'),
    # path('category/<int:category_id>/', get_category, name='category'),
    # path('news/<int:news_id>/', view_news, name='view_news'),
    # path('news/add-news/', add_news, name='add_news'),
    # path('contact/', ContactView.as_view(), name='contact'),
    # path('', cache_page(60)(HomeNews.as_view()), name='home'),
    path('register/', register, name='register'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
    path('contact/', contact, name='contact'),
    path('', HomeNews.as_view(), name='home'),
    path('category/<int:category_id>/', NewsByCategory.as_view(), name='category'),
    path('news/<int:pk>/', ViewNews.as_view(), name='view_news'),
    path('news/add-news/', CreateNews.as_view(), name='add_news'),
    path('profile/', ViewProfile.as_view(), name='profile'),
    path('profile/update-news/<int:pk>/', UpdateNewsView.as_view(), name='update_news'),
    path('profile/delete-news/<int:pk>/', DeleteNewsView.as_view()),
]
