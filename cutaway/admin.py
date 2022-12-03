from django.contrib import admin

from .models import Message, Board, Topic, Post, News

# Добавление модели на главную страницу интерфейса администратора
admin.site.register(Message)
admin.site.register(Board)
admin.site.register(Topic)
admin.site.register(Post)
admin.site.register(News)
