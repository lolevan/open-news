# -*- coding: UTF-8 -*-
# get_object_or_404
from django.urls import reverse_lazy
# from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, CreateView, FormView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.contrib.auth import login, logout
from django.core.mail import send_mail, get_connection

from testsite.settings import EMAIL_HOST_USER

from .models import News, Category

from .forms import NewsForm, UserRegisterForm, UserLoginForm, ContactForm

from .utils import MyMixin


class HomeNews(MyMixin, ListView):
    """
    This class shows Objects in all category
    """
    model = News
    template_name = 'news/home_news_list.html'
    context_object_name = 'news'
    mixin_pro = 'hello world'
    # extra_context = {'title': 'Главная'}
    paginate_by = 2

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(HomeNews, self).get_context_data(**kwargs)
        context['title'] = self.get_upper('Главная страница')
        context['mixin_prop'] = self.get_prop()
        return context

    def get_queryset(self):
        return News.objects.filter(is_published=True).select_related('category')


class NewsByCategory(MyMixin, ListView):
    """
    This class shows Objects in its category
    """
    model = News
    template_name = 'news/home_news_list.html'
    context_object_name = 'news'
    allow_empty = False
    # extra_context = {'title': 'Да тайтл'}
    paginate_by = 2

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(NewsByCategory, self).get_context_data(**kwargs)
        context['title'] = self.get_upper(Category.objects.get(pk=self.kwargs['category_id']))
        return context

    def get_queryset(self):
        return News.objects.filter(category_id=self.kwargs['category_id'], is_published=True).select_related('category')


class ViewNews(DetailView):
    """
    This class View object in the interface
    """
    model = News
    context_object_name = 'news_item'
    # pk_url_kwarg = 'news_id'
    # template_name = 'news/news_detail.html'


class CreateNews(CreateView, LoginRequiredMixin):
    """
    This class Create Object in the interface
    """
    form_class = NewsForm
    template_name = 'news/add_news.html'
    # login_url = '/admin/'
    # success_url = reverse_lazy('home')
    raise_exception = True
    # fields = '__all__'

    def get_context_data(self, **kwargs):
        context = super(CreateNews, self).get_context_data(**kwargs)
        context['action'] = 'Добавление'
        return context

    def form_valid(self, form):
        """
        relation of the object to the author
        """
        form.instance.author = self.request.user
        return super(CreateNews, self).form_valid(form)


class ViewProfile(ListView, LoginRequiredMixin):
    """
    Viewing a profile in posts
    """
    model = News
    context_object_name = 'profile_items'
    template_name = 'news/profile.html'
    raise_exception = True
    paginate_by = 3

    def get_queryset(self):
        return News.objects.filter(author=self.request.user).select_related('category')


class UpdateNewsView(UpdateView):
    """
    Update posts
    """
    model = News
    form_class = NewsForm
    template_name = 'news/add_news.html'

    def get_context_data(self, **kwargs):
        context = super(UpdateNewsView, self).get_context_data(**kwargs)
        context['action'] = 'Обновление'
        return context

    def get_queryset(self):
        """
        Restricts access to posts
        """
        base_qs = super(UpdateNewsView, self).get_queryset()
        return base_qs.filter(author=self.request.user)


class DeleteNewsView(DeleteView):
    """
    Deleting posts
    """
    model = News
    template_name = 'news/news_confirm_delete.html'
    success_url = reverse_lazy('profile')

    def get_queryset(self):
        """
        Restricts access to posts
        """
        base_qs = super(DeleteNewsView, self).get_queryset()
        return base_qs.filter(author=self.request.user)


def contact(request):
    """
    This function allows you to make a newsletter
    """
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            mail = send_mail(
                form.cleaned_data['subject'],
                f"{form.cleaned_data['content']} "
                f"\nС уважением {form.cleaned_data['email']}",
                EMAIL_HOST_USER,
                ['vanechka-nikitin-2004@mail.ru'],
                fail_silently=True,
            )
            user_mail = send_mail(
                'Благодарственное письмо',
                'Ваш запрос отправлен, благодарим за обратную связь.',
                EMAIL_HOST_USER,
                [form.cleaned_data['email']],
                fail_silently=True,
            )

            if mail:
                if user_mail:
                    messages.success(request, 'Письмо отправлено')
                    return redirect('contact')
                else:
                    messages.error(request, 'Недействительная почта')
            else:
                messages.error(request, 'Ошибка отправки')
        else:
            messages.error(request, 'Ошибка валидации')
    else:
        form = ContactForm()
    return render(request, 'news/test.html', {'form': form})


def register(request):
    """
    This function register User in the interface
    """
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Вы успешно зарегистрировались')
            return redirect('home')
        else:
            messages.error(request, 'Ошибка регистрации')
    else:
        form = UserRegisterForm()
    return render(request, 'news/register.html', {'form': form})


def user_login(request):
    """
    This function login the User in the interface
    """
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = UserLoginForm()
    return render(request, 'news/login.html', {'form': form})


def user_logout(request):
    """
    This function logout from the interface
    """
    logout(request)
    return redirect('login')


# class ContactView(FormView):
#     form_class = ContactForm
#     template_name = 'news/test.html'
#
#     success_url = reverse_lazy('contact')
#
#     def form_valid(self, form):
#         mail = send_mail(
#             form.cleaned_data['subject'],
#             f"{form.cleaned_data['content']} "
#             f"\nС уважением {form.cleaned_data['email']}",
#             EMAIL_HOST_USER,
#             ['vanechka-nikitin-2004@mail.ru'],
#             fail_silently=True,
#         )
#         user_mail = send_mail(
#             'Благодарственное письмо',
#             'Ваш запрос отправлен, благодарим за обратную связь.',
#             EMAIL_HOST_USER,
#             [form.cleaned_data['email']],
#             fail_silently=True,
#         )
#
#         if mail:
#             if user_mail:
#                 messages.success(self.request, 'Письмо отправлено')
#                 return redirect('contact')
#             else:
#                 messages.error(self.request, 'Недействительная почта')
#         else:
#             messages.error(self.request, 'Ошибка отправки')
#         # ContactForm(request.POST)
#         return super(ContactView, self).form_valid(form)


# def index(request):
#     news = News.objects.all()
#     context = {
#         'news': news,
#         'title': 'News list',
#     }
#     return render(request, 'news/index.html', context)


# def get_category(request, category_id):
#     news = News.objects.filter(category_id=category_id)
#     category = Category.objects.get(pk=category_id)
#     context = {
#         'news': news,
#         'category': category,
#     }
#     return render(request, 'news/category.html', context)


# def view_news(request, news_id):
#     # news_item = News.objects.get(pk=news_id)
#     news_item = get_object_or_404(News, pk=news_id)
#     return render(request, 'news/view_news.html', {'news_item': news_item})


# def add_news(request):
#     if request.method == 'POST':
#         form = NewsForm(request.POST)
#         if form.is_valid():
#             # print(form.cleaned_data)
#             # news = News.objects.create(**form.cleaned_data)
#             news = form.save()
#             return redirect(news)
#     else:
#         form = NewsForm()
#     return render(request, 'news/add_news.html', {'form': form})
