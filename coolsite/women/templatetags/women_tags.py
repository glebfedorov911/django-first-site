from django import template
from django.db.models import Count

from women.models import *

register = template.Library()

# @register.simple_tag(name='getcats')
# def get_categories(filter=None):
#     if filter:
#         return Category.objects.filter(pk=filter)
#     return Category.objects.all()

@register.inclusion_tag('women/list_categories.html')
def show_categories(sort=None, cat_selected=0):
    if not sort:
        cats = Category.objects.all()
    else:
        cats = Category.objects.order_by(sort)

    return {'cats':cats, 'cat_selected':cat_selected, 'list_values': not_empty_category}

def not_empty_category():
    values_cat_id = Women.objects.values('cat_id').annotate(Count('id'))  # отображение не пустых категорий
    # запрос возвращает словарь со значение cat_id и количеством их в таблице
    list_values = [values_cat_id[idx]['cat_id'] for idx in range(len(values_cat_id))]

    return list_values

# @register.simple_tag()
# def show_menu():
#     menu = [{'title': 'О сайте', 'url_name': 'about'},
#             {'title': 'Добавить статью', 'url_name': 'add_page'},
#             {'title': 'Обратная связь', 'url_name': 'contact'},
#             {'title': 'Войти', 'url_name': 'login'},
#             ]
#     return menu

@register.inclusion_tag('women/menu.html') #{% new_menu %} в html файле прописать (до этого создать html в шаблонах this.file:menu.html)
def new_menu():
    menu = [{'title': 'О сайте', 'url_name': 'about'},
            {'title': 'Добавить статью', 'url_name': 'add_page'},
            {'title': 'Обратная связь', 'url_name': 'contact'},
            {'title': 'Войти', 'url_name': 'login'},
            ]
    return {'menu':menu}