# -*- coding: UTF-8 -*-
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django import forms

from captcha.fields import CaptchaField, CaptchaTextInput

from .models import News

from re import match


class ContactForm(forms.Form):
    subject = forms.CharField(
        label='Тема',
        widget=forms.TextInput(attrs={'class': 'form-control'}),
    )
    content = forms.CharField(label='Текст', widget=forms.Textarea(
         attrs={
             "class": "form-control",
             "rows": 5
         }))
    captcha = CaptchaField()


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(
        label='Имя пользывателя',
        widget=forms.TextInput(attrs={'class': 'form-control'}),
    )
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(
        attrs={'class': 'form-control'}
    ))


class UserRegisterForm(UserCreationForm):
    username = forms.CharField(
        label='Имя пользывателя',
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        help_text='Максимум 150 символов'
    )
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput(
        attrs={'class': 'form-control'}
    ))
    password2 = forms.CharField(label='Подтверждение пароля', widget=forms.PasswordInput(
        attrs={'class': 'form-control'}
    ))
    email = forms.EmailField(label='E-mail', widget=forms.EmailInput(
        attrs={'class': 'form-control', 'rows': 5}
    ))

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
        # widgets = {
        #     'username': forms.TextInput(attrs={'class': 'form-control'}),
        #     'email': forms.EmailInput(attrs={'class': 'form-control', 'rows': 5}),
        #     'password1': forms.PasswordInput(attrs={'class': 'form-control'}),
        #     'password2': forms.PasswordInput(attrs={'class': 'form-control'}),
        # }


class NewsForm(forms.ModelForm):
    class Meta:
        model = News
        # fields = '__all__'
        fields = ['title', 'content', 'is_published', 'category']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
            'category': forms.Select(attrs={'class': 'form-control'}),
        }

    def clean_title(self):
        title = self.cleaned_data['title']
        if match(r'\d', title):
            raise ValidationError('Название не должно начинаться с цифры')
        return title

# class NewsForm(forms.Form):
#     title = forms.CharField(max_length=150, label='Название', widget=forms.TextInput(
#     attrs={"class": "form-control"
#     }))
#     content = forms.CharField(label='Текст', required=False, widget=forms.Textarea(
#     attrs={
#         "class": "form-control",
#         "rows": 5
#     }))
#     is_published = forms.BooleanField(label='Опубликовано?', initial=True)
#     category = forms.ModelChoiceField(empty_label='Выберите категорию', label='Категория',
#                                       queryset=Category.objects.all(), widget=forms.Select(attrs={
#                                       "class": "form-control"
#                                       }))
