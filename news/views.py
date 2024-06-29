# -*- coding: UTF-8 -*-
# get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.urls import reverse_lazy
# from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, FormView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from django.contrib.auth import login, logout
from django.core.mail import send_mail, get_connection
from django.contrib.auth.models import AnonymousUser

from testsite.settings import EMAIL_HOST_USER

from .models import News, Category, Rating, Comment

from .forms import NewsForm, UserRegisterForm, UserLoginForm, ContactForm, CommentForm

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

        # Добавляем среднюю оценку для каждого поста в контекст
        for news_item in context['news']:
            news_item.average_rating = news_item.average_rating()

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
    model = News
    context_object_name = 'news_item'
    template_name = 'news/view_news.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comment_form'] = CommentForm()  # Добавляем форму комментария в контекст

        # Добавляем значение оценки пользователя, если она существует
        news_item = self.get_object()

        if self.request.user.is_authenticated:
            user_rating = Rating.objects.filter(user=self.request.user, news=news_item).first()
            initial_rating = user_rating.value if user_rating else None
        else:
            initial_rating = None

        context['initial_rating'] = initial_rating

        # Добавляем news_id в контекст, чтобы он был доступен в шаблоне
        context['news_id'] = news_item.pk

        # Добавляем среднюю оценку в контекст
        context['average_rating'] = news_item.average_rating()

        return context

    def post(self, request, *args, **kwargs):
        news_item = self.get_object()
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.news = news_item
            comment.author = request.user

            parent_id = request.POST.get('parent_id')
            if parent_id:
                comment.parent_id = parent_id

            comment.save()
            return redirect(news_item)

        else:
            context = self.get_context_data()
            context['comment_form'] = form
            return self.render_to_response(context)


@login_required
def rate_news(request, news_id):
    news = get_object_or_404(News, pk=news_id)
    if request.user.is_authenticated:  # Проверяем, аутентифицирован ли пользователь
        user_rating = Rating.objects.filter(user=request.user, news=news).first()
        initial_rating = user_rating.value if user_rating else None

        if request.method == 'POST':
            rating_value = int(request.POST.get('rating'))
            rating, created = Rating.objects.get_or_create(user=request.user, news=news)
            rating.value = rating_value
            rating.save()
            return redirect('view_news', pk=news_id)

        return render(request, 'view_news.html', {'news': news, 'initial_rating': initial_rating})
    else:
        return HttpResponseForbidden()


class CreateNews(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    """
    This class Create Object in the interface
    """
    form_class = NewsForm
    template_name = 'news/add_news.html'
    raise_exception = True
    success_url = reverse_lazy('home')

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

    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.is_staff

    def handle_no_permission(self):
        if self.raise_exception:
            from django.core.exceptions import PermissionDenied
            raise PermissionDenied
        return redirect('login')  # или любая другая страница для перенаправления


class ViewProfile(ListView, LoginRequiredMixin):
    """
    Viewing a profile in posts
    """
    model = Comment
    context_object_name = 'profile_items'
    template_name = 'news/profile.html'
    paginate_by = 3

    def get_queryset(self):
        # Получаем все комментарии пользователя
        user_comments = Comment.objects.filter(author=self.request.user)

        # Создаем список для хранения связанных с комментариями оценок
        profile_items = []

        # Для каждого комментария получаем связанный пост и оценку
        for comment in user_comments:
            post = comment.news
            rating = Rating.objects.filter(user=self.request.user, news=post).first()
            rating_value = rating.value if rating else None
            profile_items.append({'post': post, 'comment': comment, 'rating_value': rating_value})

        return profile_items


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
