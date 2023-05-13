from django.db import models
from django.urls import reverse
from PIL import Image

from coolsite import settings


# python manage.py shell
# from django.db import connection (connection.queries)
# from women.models import Women
# Women.objects.filter(pk__gte=2) or (pk__lte=2)
# gte - >= lte - <=

# get и filter - get - генерирует исключение, а filter всегда вернет список (пустой или нет)

# filter - фильтер, exclude - обратный фильтер
# delete - удалить, create - создать
# get - получить

class Women(models.Model):
    title = models.CharField(max_length=255, verbose_name='Заголовок')
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name='URL')
    content = models.TextField(blank=True, verbose_name='Текст статьи')
    photo = models.ImageField(upload_to='photos/%Y/%m/%d/', verbose_name='Фото')
    time_create = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    time_update = models.DateTimeField(auto_now=True, verbose_name='Дата последнего редактирования')
    is_published = models.BooleanField(default=True, verbose_name='Публикация')
    cat = models.ForeignKey('Category', on_delete=models.PROTECT, verbose_name='Категория', related_name='get_posts')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post', kwargs={'post_slug': self.slug})

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        standart = (250, 350)

        img = Image.open(self.photo)
        width_photo, height_photo = img.size
        if width_photo > standart[0] or height_photo > standart[1]:
            img.thumbnail(standart)

        img.save(self.photo.path, 'PNG')
        img.close()

    class Meta:
        verbose_name = 'Известные женщины'
        verbose_name_plural = 'Известные женщины'
        ordering = ['-time_create', 'title']

class Category(models.Model):
    name = models.CharField(max_length=100, db_index=True, verbose_name='Название категории')
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name='URL')

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('category', kwargs={'cat_slug': self.slug})

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ['pk']

class Comment(models.Model):
    name = models.CharField(max_length=255, verbose_name='Имя пользователя')
    text = models.TextField(verbose_name='Комментарий')
    post = models.ForeignKey('Women', on_delete=models.PROTECT, verbose_name='Пост')
    time_create = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')

    def __str__(self):
        return self.text

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ['-pk']

class Contact(models.Model):
    name = models.CharField(max_length=255, verbose_name='Имя отправителя')
    email = models.EmailField(verbose_name='Почта')
    message = models.TextField(verbose_name='Сообщение')
    is_check = models.BooleanField(default=False, verbose_name='Статус ответа', auto_created=True)

    def __str__(self):
        return self.message

    class Meta:
        verbose_name = 'Обратная связь'
        verbose_name_plural = 'Обратные связи'