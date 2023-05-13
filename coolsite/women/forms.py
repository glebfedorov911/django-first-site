from captcha.fields import CaptchaField
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from emoji_picker.widgets import *

from .models import *
from .utils import *


# class AddPostForm(forms.Form):
#     title = forms.CharField(max_length=255, label='Заголовок', widget=forms.TextInput(attrs={'class':'form-input'}))
#     slug = forms.SlugField(max_length=255, label = 'URL')
#     content = forms.CharField(widget=forms.Textarea(attrs={'cols':60, 'rows':10}), label='Текст статьи')
#     is_published = forms.BooleanField(label='Публикация', required=False, initial=True)
#     cat = forms.ModelChoiceField(queryset=Category.objects.all(), label='Категории', empty_label='Категория не выбрана')

class AddPostForm(FormMixin, forms.ModelForm):
    content = forms.CharField(label='Текст статьи')
    captcha = CaptchaField(label='Капча')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['cat'].empty_label = 'Категория не выбрана'

    class Meta:
        model = Women
        fields = ['title', 'slug', 'content', 'photo', 'is_published', 'cat']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-input'}),
            'content': forms.Textarea(attrs={'cols': 60, 'rows': 10}),
        }

    def clean_title(self):
        title = self.cleaned_data['title']
        self.clean_title_from_form(title)

        return title

    def clean_photo(self):
        photo = self.cleaned_data['photo']
        self.clean_photo_from_form(photo)

        return photo


class RegisterUserForm(UserCreationForm):
    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={'class': 'form-input'}))
    email = forms.EmailField(label='Почта', widget=forms.EmailInput(attrs={'class': 'form-input'}))
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-input'}))
    password2 = forms.CharField(label='Повтор пароля', widget=forms.PasswordInput(attrs={'class': 'form-input'}))
    captcha = CaptchaField(label='Капча')

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

        # widgets = { #НЕ РАБОТАЕТ, РАБОТАЕТ КАК ВЫШЕ(ТОЛЬКО С РЕГИСТРАЦИЕЙ ТАК)
        #     'username': forms.TextInput(attrs={'class':'form-input'}),
        #     'password1': forms.PasswordInput(attrs={'class': 'form-input'}),
        #     'password2': forms.PasswordInput(attrs={'class': 'form-input'}),
        # }


class LoginUserForm(AuthenticationForm):
    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={'class': 'form-input'}))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-input'}))
    captcha = CaptchaField(label='Капча')

    class Meta:
        model = User
        fields = ('username', 'password')


# class ContactForm(forms.Form):
#     name = forms.CharField(label='Имя', max_length=255)
#     email = forms.EmailField(label='Email')
#     content = forms.CharField(label='Текст', widget=forms.Textarea(attrs={'cols': 60, 'rows': 10}))
#     captcha = CaptchaField(label='Капча')

class ContactForm(forms.ModelForm):
    captcha = CaptchaField(label='Капча')

    class Meta:
        model = Contact
        fields = ('name', 'email', 'message')
        widgets = {
            'message':forms.Textarea(attrs={'cols': 60, 'rows': 10}),
        }

class CommentForm(forms.ModelForm):
    text = forms.CharField(label='Комментарий', widget=EmojiPickerTextareaAdmin)

    class Meta:
        model = Comment
        fields = ('text', )


class EditPostForm(FormMixin, forms.ModelForm):
    captcha = CaptchaField(label='Капча')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    class Meta:
        model = Women
        fields = ('title', 'content', 'photo', 'is_published', 'cat')

    def clean_photo(self):
        try:
            photo = self.files['photo']
        except:
            return
        return self.clean_photo_from_form(photo)

    def clean_title(self):
        title = self.data['title']
        return self.clean_title_from_form(title)
