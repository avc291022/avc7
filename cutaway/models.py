from django.db import models
#from django.utils.translation import ugettext as _
from django.utils.translation import gettext_lazy as _

from PIL import Image
from PIL import ImageFile
ImageFile.LOAD_TRUNCATED_IMAGES = True
from django.core.files.storage import default_storage as storage  

from django.contrib.auth.models import User

import math

# Модели отображают информацию о данных, с которыми вы работаете.
# Они содержат поля и поведение ваших данных.
# Обычно одна модель представляет одну таблицу в базе данных.
# Каждая модель это класс унаследованный от django.db.models.Model.
# Атрибут модели представляет поле в базе данных.
# Django предоставляет автоматически созданное API для доступа к данным

# choices (список выбора). Итератор (например, список или кортеж) 2-х элементных кортежей,
# определяющих варианты значений для поля.
# При определении, виджет формы использует select вместо стандартного текстового поля
# и ограничит значение поля указанными значениями.

# Читабельное имя поля (метка, label). Каждое поле, кроме ForeignKey, ManyToManyField и OneToOneField,
# первым аргументом принимает необязательное читабельное название.
# Если оно не указано, Django самостоятельно создаст его, используя название поля, заменяя подчеркивание на пробел.
# null - Если True, Django сохранит пустое значение как NULL в базе данных. По умолчанию - False.
# blank - Если True, поле не обязательно и может быть пустым. По умолчанию - False.
# Это не то же что и null. null относится к базе данных, blank - к проверке данных.
# Если поле содержит blank=True, форма позволит передать пустое значение.
# При blank=False - поле обязательно.

# Сообщения в чат
class Message(models.Model):
    datem = models.DateTimeField(_('datem'), auto_now_add=True)
    sender = models.ForeignKey(User, related_name='sender_message', on_delete=models.CASCADE)
    recipient = models.ForeignKey(User, related_name='recipient_message', on_delete=models.CASCADE)
    details = models.TextField(_('message_details'), blank=True, null=True)
    class Meta:
        # Параметры модели
        # Переопределение имени таблицы
        db_table = 'message'
        # indexes - список индексов, которые необходимо определить в модели
        indexes = [
            models.Index(fields=['sender']),
            models.Index(fields=['recipient']),
        ]
        # Сортировка по умолчанию
        ordering = ['-datem']

# Раздел форума
class Board(models.Model):
    name = models.CharField(_('board_name'), max_length=128, unique=True)
    description = models.TextField(_('board_description'))
    class Meta:
        # Параметры модели
        # Переопределение имени таблицы
        db_table = 'board'
    def __str__(self):
        return self.name

# Тема форума   
class Topic(models.Model):
    subject = models.CharField(_('topic_subject'), max_length=255)
    last_updated = models.DateTimeField(_('last_updated'), auto_now_add=True)
    board = models.ForeignKey(Board, related_name='topics', on_delete=models.CASCADE)
    starter = models.ForeignKey(User, related_name='topics', on_delete=models.CASCADE)
    views = models.PositiveIntegerField(_('views'), default=0)
    class Meta:
        # Параметры модели
        # Переопределение имени таблицы
        db_table = 'topic'
    def __str__(self):
        return self.subject
    def get_page_count(self):
        count = self.posts.count()
        pages = count / 20
        return math.ceil(pages)
    def has_many_pages(self, count=None):
        if count is None:
            count = self.get_page_count()
        return count > 6
    def get_page_range(self):
        count = self.get_page_count()
        if self.has_many_pages(count):
            return range(1, 5)
        return range(1, count + 1)

# Сообщение (POST) для форума
class Post(models.Model):
    message = models.TextField(_('message'),max_length=4000)
    topic = models.ForeignKey(Topic, related_name='posts', on_delete=models.CASCADE)
    created_at = models.DateTimeField(_('created_at'),auto_now_add=True)
    updated_at = models.DateTimeField(_('updated_at'),null=True)
    created_by = models.ForeignKey(User, related_name='posts', on_delete=models.CASCADE)
    updated_by = models.ForeignKey(User, null=True, related_name='+', on_delete=models.CASCADE)
    class Meta:
        # Параметры модели
        # Переопределение имени таблицы
        db_table = 'post'
    def __str__(self):
        truncated_message = Truncator(self.message)
        return truncated_message.chars(30)


# Новости 
class News(models.Model):
    daten = models.DateTimeField(_('daten'))
    title = models.CharField(_('title_news'), max_length=256)
    details = models.TextField(_('details_news'))
    photo = models.ImageField(_('photo_news'), upload_to='images/', blank=True, null=True)    
    class Meta:
        # Параметры модели
        # Переопределение имени таблицы
        db_table = 'news'
        # indexes - список индексов, которые необходимо определить в модели
        indexes = [
            models.Index(fields=['daten']),
        ]
        # Сортировка по умолчанию
        ordering = ['daten']
    #def save(self):
    #    super().save()
    #    img = Image.open(self.photo.path) # Open image
    #    # resize image
    #    if img.width > 512 or img.height > 700:
    #        proportion_w_h = img.width/img.height  # Отношение ширины к высоте 
    #        output_size = (512, int(512/proportion_w_h))
    #        img.thumbnail(output_size) # Изменение размера
    #        img.save(self.photo.path) # Сохранение

# Представление базы данных Сообщения
class ViewMessage(models.Model):
    id = models.IntegerField(_('message_id'), primary_key=True)
    datem = models.DateTimeField(_('datem'))
    sender_id = models.IntegerField(_('sender_id'))
    sender_username = models.CharField(_('sender_username'), max_length=150)
    sender_first_name = models.CharField(_('sender_first_name'), max_length=150, blank=True, null=True)
    sender_last_name = models.CharField(_('sender_last_name'), max_length=150, blank=True, null=True)
    recipient_id = models.IntegerField(_('recipient_id'))
    recipient_username = models.CharField(_('recipient_username'), max_length=150)
    recipient_first_name = models.CharField(_('recipient_first_name'), max_length=150, blank=True, null=True)
    recipient_last_name = models.CharField(_('recipient_last_name'), max_length=150, blank=True, null=True)
    details = models.TextField(_('message_details'))
    class Meta:
        # Параметры модели
        # Переопределение имени таблицы
        db_table = 'view_message'
        # indexes - список индексов, которые необходимо определить в модели
        indexes = [
            models.Index(fields=['datem']),
        ]
        # Сортировка по умолчанию
        ordering = ['datem']
        # Таблицу не надо не добавлять не удалять
        managed = False


# Представление базы данных Пользователи + Последние отправленны и последние принятые сообщения
class ViewUserLastMessage(models.Model):
    id = models.IntegerField(_('auth_user_id'), primary_key=True)
    is_superuser =  models.BooleanField(_('is_superuser'), blank=True, null=True)
    username = models.CharField(_('username'), max_length=150)
    first_name = models.CharField(_('first_name'), max_length=150, blank=True, null=True)
    last_name = models.CharField(_('last_name'), max_length=150, blank=True, null=True)
    last_send_id = models.IntegerField(_('last_send_id'), blank=True, null=True)
    last_send_message = models.TextField(_('last_send_message'), blank=True, null=True)
    last_recipient_id = models.IntegerField(_('last_recipient_id'), blank=True, null=True)
    last_recipient_message = models.TextField(_('last_recipient_message'), blank=True, null=True)
    class Meta:
        # Параметры модели
        # Переопределение имени таблицы
        db_table = 'view_user_last_message'
        # indexes - список индексов, которые необходимо определить в модели
        indexes = [
            models.Index(fields=['username']),
        ]
        # Сортировка по умолчанию
        ordering = ['username']
        # Таблицу не надо не добавлять не удалять
        managed = False
