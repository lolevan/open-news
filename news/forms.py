# -*- coding: UTF-8 -*-
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django import forms

from captcha.fields import CaptchaField, CaptchaTextInput

from .models import News

from re import match


class ContactForm(forms.Form):
    """
    This form to contacts admins
    """
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
    """
    This is the user login form
    """
    username = forms.CharField(
        label='Имя пользывателя',
        widget=forms.TextInput(attrs={'class': 'form-control'}),
    )
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(
        attrs={'class': 'form-control'}
    ))


class UserRegisterForm(UserCreationForm):
    """
    This is the user registration form
    """
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
        """
        Form description
        """
        model = User
        fields = ('username', 'email', 'password1', 'password2')
        # widgets = {
        #     'username': forms.TextInput(attrs={'class': 'form-control'}),
        #     'email': forms.EmailInput(attrs={'class': 'form-control', 'rows': 5}),
        #     'password1': forms.PasswordInput(attrs={'class': 'form-control'}),
        #     'password2': forms.PasswordInput(attrs={'class': 'form-control'}),
        # }


class NewsForm(forms.ModelForm):
    """
    Is a form for a creating news objects
    """
    class Meta:
        """
        Form description
        """
        model = News
        # fields = '__all__'
        fields = ['title', 'content', 'is_published', 'category', 'photo']
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

    def clean_content(self):
        ban_words = ['архипиздрит', 'басран', 'бздение', 'бздеть', 'бздех', 'бзднуть', 'бздун', 'бздунья', 'бздюха', 'бикса', 'блежник', 'блудилище', 'бляд', 'блябу', 'блябуду', 'блядун', 'блядунья', 'блядь', 'блядюга', 'взьебка', 'волосянка', 'взьебывать', "вз'ебывать", 'выблядок', 'выблядыш', 'выебать', 'выеть', 'выпердеть', 'высраться', 'выссаться', 'говенка', 'говенный', 'говешка', 'говназия', 'говнецо', 'говно', 'говноед', 'говночист', 'говнюк', 'говнюха', 'говнядина', 'говняк', 'говняный', 'говнять', 'гондон', 'дермо', 'долбоеб', 'дрисня', 'дрист', 'дристать', 'дристануть', 'дристун', 'дристуха', 'дрочена', 'дрочила', 'дрочилка', 'дрочить', 'дрочка', 'ебало', 'ебальник', 'ебануть', 'ебаный', 'ебарь', 'ебатория', 'ебать', 'ебаться', 'ебец', 'ебливый', 'ебля', 'ебнуть', 'ебнуться', 'ебня', 'ебун', 'елда', 'елдак', 'елдачить', 'заговнять', 'задристать', 'задрока', 'заеба', 'заебанец', 'заебать', 'заебаться', 'заебываться', 'заеть', 'залупа', 'залупаться', 'залупить', 'залупиться', 'замудохаться', 'засерун', 'засеря', 'засерать', 'засирать', 'засранец', 'засрун', 'захуячить', 'злоебучий', 'изговнять', 'изговняться', 'кляпыжиться', 'курва', 'курвенок', 'курвин', 'курвяжник', 'курвяжница', 'курвяжный', 'манда', 'мандавошка', 'мандей', 'мандеть', 'мандища', 'мандюк', 'минет', 'минетчик', 'минетчица', 'мокрохвостка', 'мокрощелка', 'мудак', 'муде', 'мудеть', 'мудила', 'мудистый', 'мудня', 'мудоеб', 'мудозвон', 'муйня', 'набздеть', 'наговнять', 'надристать', 'надрочить', 'наебать', 'наебнуться', 'наебывать', 'нассать', 'нахезать', 'нахуйник', 'насцать', 'обдристаться', 'обдристаться', 'обосранец', 'обосрать', 'обосцать', 'обосцаться', 'обсирать', 'опизде', 'отпиздячить', 'отпороть', 'отъеть', 'охуевательский', 'охуевать', 'охуевающий', 'охуеть', 'охуительный', 'охуячивать', 'охуячить', 'педрик', 'пердеж', 'пердение', 'пердеть', 'пердильник', 'перднуть', 'пердун', 'пердунец', 'пердунина', 'пердунья', 'пердуха', 'пердь', 'передок', 'пернуть', 'пидор', 'пизда', 'пиздануть', 'пизденка', 'пиздеть', 'пиздить', 'пиздища', 'пиздобратия', 'пиздоватый', 'пиздорванец', 'пиздорванка', 'пиздострадатель', 'пиздун', 'пиздюга', 'пиздюк', 'пиздячить', 'писять', 'питишка', 'плеха', 'подговнять', 'подъебнуться', 'поебать', 'поеть', 'попысать', 'посрать', 'поставить', 'поцоватый', 'презерватив', 'проблядь', 'проебать', 'промандеть', 'промудеть', 'пропиздеть', 'пропиздячить', 'пысать', 'разъеба', 'разъебай', 'распиздай', 'распиздеться', 'распиздяй', 'распроеть', 'растыка', 'сговнять', 'секель', 'серун', 'серька', 'сика', 'сикать', 'сикель', 'сирать', 'сирывать', 'скурвиться', 'скуреха', 'скурея', 'скуряга', 'скуряжничать', 'спиздить', 'срака', 'сраный', 'сранье', 'срать', 'срун', 'ссака', 'ссаки', 'ссать', 'старпер', 'струк', 'суходрочка', 'сцавинье', 'сцака', 'сцаки', 'сцание', 'сцать', 'сциха', 'сцуль', 'сцыха', 'сыкун', 'титечка', 'титечный', 'титка', 'титочка', 'титька', 'трипер', 'триппер', 'уеть', 'усраться', 'усцаться', 'фик', 'фуй', 'хезать', 'хер', 'херня', 'херовина', 'херовый', 'хитрожопый', 'хлюха', 'хуевина', 'хуевый', 'хуек', 'хуепромышленник', 'хуерик', 'хуесос', 'хуище', 'хуй', 'хуйня', 'хуйрик', 'хуякать', 'хуякнуть', 'целка', 'шлюха']
        content = self.cleaned_data['content']
        if set(ban_words) & set(content.split()):
            raise ValidationError('Нецензурные слова мягко обходятся в этом сообществе')
        return content

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
