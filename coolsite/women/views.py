import json
import time
from collections import OrderedDict

from django.contrib.auth import logout, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.views import LoginView
from django.core import serializers
from django.db.models import Count
from django.forms import model_to_dict
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseNotFound, Http404, HttpResponseRedirect, JsonResponse
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, FormView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin #Запрет не авторизованным пользователям посещать страницу
from django.core.paginator import Paginator
from django.core.mail import send_mail

from .forms import *
from .models import *
from .utils import *
 #!!!!!!!!!!!!!!!!!!ИСПОЛЬЗОВАТЬ DEBUG TOOLBAR!!!!!!!!!!!!!!!!!!!!
#raise Http404() - ошибка redirect - перенаправление

# def index(request):
#     posts = Women.objects.all()
#
#     context = {
#         'posts': posts,
#         'title': 'Главная страница',
#         'cat_selected': 0,
#     }
#
#     return render(request, 'women/index.html', context=context)

class WomenHome(DataMixin, ListView):
    model = Women
    template_name = 'women/index.html'
    context_object_name = 'posts'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Главная страница', cat_selected=0)
        return dict(list(context.items())+list(c_def.items()))

    def get_queryset(self):
        return Women.objects.filter(is_published=True).select_related('cat')

# @login_required #Запрет не авторизованным пользователям посещать страницу
# def about(request):
#     # contact_list = Women.objects.all()
#     # paginator = Paginator(contact_list, 3)
#     # page_number = request.GET.get('page')
#     # page_obj = paginator.get_page(page_number) #ПАГИНАЦИЯ  В ФУНКЦИЯХ
#     return render(request, 'women/about.html', {'title':'О сайте', 'page_obj':page_obj}) #'page_obj':page_obj

class About(DataMixin, TemplateView):
    template_name = 'women/about.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='О сайте')
        return dict(list(context.items()) + list(c_def.items()))

# def addpage(request):
#     if request.method == 'POST':
#         form = AddPostForm(request.POST, request.FILES)
#         if form.is_valid():
#             # print(form.cleaned_data)
#             # try:
#             #     Women.objects.create(**form.cleaned_data)
#             #     return redirect('home')
#             # except:
#             #     form.add_error(None, 'Ошибка добавления поста')
#             form.save()
#             return redirect('home')
#     else:
#         form = AddPostForm()
#     return render(request, 'women/addpage.html', {'title':'Добавление статьи', 'form':form})


class AddPage(LoginRequiredMixin, DataMixin, CreateView):
    form_class = AddPostForm
    template_name = 'women/addpage.html'
    success_url = reverse_lazy('home') #get_absolute_url перенаправляет в статью
    login_url = reverse_lazy('home')
    # raise_exception = True #ERROR 403 (ДОСТУП ЗАПРЕЩЕН)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Добавление статьи')
        return dict(list(context.items())+list(c_def.items()))

# def contact(request):
#     return HttpResponse('Обратная связь')

class ContactFormView(DataMixin, FormView):
    form_class = ContactForm
    template_name = 'women/contact.html'
    success_url = reverse_lazy('home')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Обратная связь')
        return dict(list(context.items())+list(c_def.items()))

    def form_valid(self, form):
        form.save()
        return redirect('home')

    # def login(request):
#     return HttpResponse('Авторизация')

def pageNotFound(request, exception):
    return HttpResponseNotFound('<h1>Страница не найдена</h1>')


# def show_post(request, post_slug):
#     post = get_object_or_404(Women, slug=post_slug)
#
#     context = {
#         'post': post,
#         'title': post.title,
#         'cat_selected': post.cat_id,
#     }
#
#     return render(request, 'women/post.html', context=context)


class ShowPost(DataMixin, DetailView):
    model = Women
    template_name = 'women/post.html'
    slug_url_kwarg = 'post_slug'
    # pk_url_kwarg = 'post_pk'
    context_object_name = 'post'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)

        page_obj = self.get_paginate(context['post'])
        post_edit = self.edit_form(context['post'])

        c_def = self.get_user_context(title=context['post'], cat_selected=context['post'].cat_id,
                                      form=CommentForm, post_slug=context['post'].slug,
                                      page_obj_=page_obj, form_edit=post_edit)

        return dict(list(context.items())+list(c_def.items()))

    def post(self, *args, **kwargs):
        if self.request.method == 'POST' and is_ajax(self.request):
            new_comments = Comment.objects.create(text=self.request.POST['comment_text'], post=self.get_object(),
                                                  name=self.request.user.username)
            new_comments.save()
            return HttpResponse()


        if self.request.method == 'POST' and 'edit_form' in self.request.POST:
            form_edit = self.edit_form(self.get_object(), self.request.POST, self.request.FILES)
            if form_edit.is_valid():
                form_edit.save()
            else:
                return redirect('not_valid_data')

        return redirect('post', self.kwargs['post_slug'])

    def get_paginate(self, obj):
        queryset = Comment.objects.filter(post=obj)
        paginator = Paginator(queryset, 2)
        page_nums = self.request.GET.get('comment_page')
        page_obj = paginator.get_page(page_nums)
        return page_obj

    def edit_form(self, obj, *args):
        return EditPostForm(*args, instance=obj)

# def show_category(request, cat_slug):
#     cat = Category.objects.get(slug=cat_slug)
#     posts = Women.objects.filter(cat_id=cat.id)
#
#     context = {
#         'posts': posts,
#         'title': 'Отображение по рубрикам',
#         'cat_selected': cat.pk,
#     }
#
#     return render(request, 'women/index.html', context=context)

class WomenCategory(DataMixin, ListView):
    model = Women
    template_name = 'women/index.html'
    context_object_name = 'posts'
    allow_empty = False

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c = Category.objects.get(slug=self.kwargs['cat_slug'])
        c_def = self.get_user_context(title=f'Категория - {c.name}', cat_selected=c.pk)
        return dict(list(context.items()) + list(c_def.items()))

    def get_queryset(self):
        return Women.objects.filter(cat__slug=self.kwargs['cat_slug'], is_published=True).select_related('cat')
        # cat - ключ к другой таблице и можно через __ связаться с элементом его таблицы
        # self.kwargs - словарь передаваемых аргументов по ссылке (из html файла)

class RegisterUser(DataMixin, CreateView):
    form_class = RegisterUserForm
    template_name = 'women/register.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Регистрация')
        return dict(list(context.items())+list(c_def.items()))

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('home')

class LoginUser(DataMixin, LoginView):
    form_class = LoginUserForm
    template_name = 'women/login.html'

    def get_context_data(self, *, object_list = None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Авторизация')
        return dict(list(context.items())+list(c_def.items()))

    def get_success_url(self):
        return reverse_lazy('home')

def logout_user(request):
    logout(request)
    return redirect('home')

def not_valid_data(request):
    return HttpResponse("Невалидные данные")

def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'

# class Ajax(View):
#
#     def get(self, request):
#         text = request.GET.get('button_text')
#
#         if is_ajax(request):
#             t = time.time()
#             return JsonResponse({'seconds': t}, status=200)
#
#         return render(request, 'women/new.html')
#
#     def post(self, request):
#         card_text = request.POST.get('text')
#
#         result = f"I've got: {card_text}"
#         return JsonResponse({'data': result}, status=200)