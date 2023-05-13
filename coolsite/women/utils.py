import datetime

from captcha.fields import CaptchaField
from django.core.exceptions import ValidationError
from django.core.paginator import Paginator
from django.db.models import Count
from django.core.cache import cache

from .models import *

menu = [{'title': 'О сайте', 'url_name': 'about'},
        {'title': 'Добавить статью', 'url_name': 'add_page'},
        {'title': 'Обратная связь', 'url_name': 'contact'},
        ]

class DataMixin:
    paginate_by = 2

    def get_user_context(self, **kwargs):
        context = kwargs

        cats_show = cache.get('page_obj_cats')
        if not cats_show:
            cats_use = [cat['cat'] for cat in Women.objects.values('cat')]
            cats_show = Category.objects.filter(pk__in=cats_use)
            cache.set('page_obj_cats', cats_show, 60)

        # values_cat_id = Women.objects.values('cat_id').annotate(Count('id'))  # отображение не пустых категорий
        # list_values = [values_cat_id[idx]['cat_id'] for idx in range(len(values_cat_id))] # запрос возвращает словарь со значение cat_id и количеством их в таблице
        #
        # context['list_values'] = list_values

        queryset_cats = cats_show
        paginator = Paginator(queryset_cats, 2)
        page_nums = self.request.GET.get('cat_page')
        page_obj_cats = paginator.get_page(page_nums)

        user_menu = menu.copy()
        if not self.request.user.is_authenticated:
            user_menu.pop(1)

        context['menu'] = user_menu
        context['page_obj_cats'] = page_obj_cats
        context['year_usable'] = datetime.date.today().year

        if 'cat_selected' not in context:
            context['cat_selected'] = None

        return context

class FormMixin:

    def cleaned_data(self, *args, **kwargs):
        super().clean()

    def clean_photo_from_form(self, photo):
        formats = ['jpg', 'png', 'jpeg']
        format_photo = str(photo)[str(photo).find('.')+1:]
        successful_letter = r'abcdefghijklmnopqrstuvwxyz<>\/".|!?1234567890_- '

        photo_name = str(photo)[:str(photo).find('.')].lower()
        format_valid = all([True if ph in successful_letter else False for ph in photo_name])

        if not format_valid:
            raise ValidationError('Невозможное имя файла')
        elif format_photo not in formats:
            raise ValidationError('Неподходящий формат')

        return photo

    def clean_title_from_form(self, title):
        maximum = 50
        if len(title) > maximum:
            raise ValidationError(f'Длина превышает {maximum} символов')

        return title
