from django.shortcuts import render
from django.contrib.auth.decorators import login_required
#from django.utils.translation import ugettext as _
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.decorators import user_passes_test
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotFound

from django.utils.decorators import method_decorator
from django.views.generic import UpdateView
from django.contrib.auth.models import User
from django.urls import reverse_lazy

from django.urls import reverse

from django.contrib.auth import login as auth_login

import datetime

import time

# К форуму
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Count
from django.views.generic import ListView
from django.utils import timezone

# Подключение моделей
from django.contrib.auth.models import User, Group

from django.db import models
from django.db.models import Q

from .models import Message, ViewMessage, ViewUserLastMessage, Board, Topic, Post, News
# Подключение форм
from .forms import BoardForm, NewTopicForm, PostForm, NewsForm

from django.contrib.auth.models import AnonymousUser

# Create your views here.
# Групповые ограничения
def group_required(*group_names):
    """Requires user membership in at least one of the groups passed in."""
    def in_groups(u):
        if u.is_authenticated:
            if bool(u.groups.filter(name__in=group_names)) | u.is_superuser:
                return True
        return False
    return user_passes_test(in_groups, login_url='403')

# Стартовая страница 
def index(request):
    return render(request, "index.html")

# Контакты
def contact(request):
    return render(request, "contact.html")

# Общая информация о компании
#def about(request):
#    return render(request, "info/about.html")

# Наши партнеры (ссылки на партнеров)
def services(request):
    return render(request, "info/services.html")

# Наши партнеры (ссылки на партнеров)
def partners(request):
    return render(request, "info/partners.html")

# Наши проекты
def projects(request):
    return render(request, "info/projects.html")

# Социальная ответственность
def social(request):
    return render(request, "info/social.html")

# Фотогалерея
def photogallery(request):
    return render(request, "info/photogallery.html")

# Фотогалерея
def video(request):
    return render(request, "info/video.html")

# Карьера 
def career(request):
    return render(request, "info/career.html")

# Вакансии 
def vacancies(request):
    return render(request, "info/vacancies.html")

"""
@login_required
def user_list(request):
    # Себя в списке не показывать, суперпользоватля тоже 
    user_id = request.user.id
    user_list = User.objects.exclude(id=user_id).exclude(is_superuser=True).order_by('username')
    my_user = request.user                
    return render(request, "user/list.html", {"user_list": user_list, "my_user": my_user,  })

# Просмотр страницы read.html для просмотра объекта.
@login_required
def user_read(request, id):
    # id текущего пользователя
    my_id = request.user.id
    try:
        recipient_user = User.objects.get(id=id)
        my_user = request.user
        message = Message.objects.filter(Q(sender_id=my_id) | Q(recipient_id=my_id)).filter(Q(sender_id=id) | Q(recipient_id=id)).order_by('-datem')
        if request.method == "POST":
            mes = Message()
            mes.sender_id = my_id
            mes.recipient_id = id
            mes.details = request.POST.get("message")
            mes.save()
            return HttpResponseRedirect(reverse('user_read', args=(id,)))
        else:
            return render(request, "user/read.html", {"recipient_user": recipient_user, "my_user": my_user, "message": message, "my_id": my_id, "user_id": id })
    except User.DoesNotExist:
        return HttpResponseNotFound("<h2>User not found</h2>")
"""

# Список для изменения с кнопками создать, изменить, удалить
@login_required
def message_index(request):
    message = Message.objects.all().order_by('-datem')
    return render(request, "message/index.html", {"message": message})

# Список для просмотра
@login_required
def message_list(request):
    # Себя в списке не показывать, суперпользоватля тоже 
    my_id = request.user.id
    my_user = request.user.first_name + " " + request.user.last_name
    # Список пользователей + последние отправленные и принятые сообщения
    view_user_last_message = ViewUserLastMessage.objects.exclude(id=my_id).exclude(is_superuser=True).order_by('username')
    #view_user_last_message = ViewUserLastMessage.objects.filter(Q(last_send_id=my_id) | Q(last_recipient_id=my_id))
    return render(request, "message/list.html", {"view_user_last_message": view_user_last_message, "my_id": my_id, "my_user": my_user, })

@login_required
def message_send(request, id):
    # id текущего пользователя
    my_id = request.user.id
    try:
        recipient_user = User.objects.get(id=id)
        my_user = request.user
        message = Message.objects.filter(Q(sender_id=my_id) | Q(recipient_id=my_id)).filter(Q(sender_id=id) | Q(recipient_id=id)).order_by('-datem')
        if request.method == "POST":
            mes = Message()
            mes.sender_id = my_id
            mes.recipient_id = id
            mes.details = request.POST.get("message")
            mes.save()
            return HttpResponseRedirect(reverse('message_send', args=(id,)))
        else:
            return render(request, "message/send.html", {"recipient_user": recipient_user, "my_user": my_user, "message": message, "my_id": my_id, "user_id": id })
    except User.DoesNotExist:
        return HttpResponseNotFound("<h2>User not found</h2>")

def forum(request):
    boards = Board.objects.all()
    return render(request, 'forum/home.html', {'boards': boards})

def board_topics(request, pk):
    board = get_object_or_404(Board, pk=pk)
    topics = board.topics.order_by('-last_updated').annotate(replies=Count('posts') - 1)
    return render(request, 'forum/topics.html', {'board': board, 'topics': topics})

# Список для изменения с кнопками создать, изменить, удалить
@login_required
@group_required("Managers")
def board_index(request):
    board = Board.objects.all().order_by('name')
    return render(request, "board/index.html", {"board": board})

# В функции create() получаем данные из запроса типа POST, сохраняем данные с помощью метода save()
# и выполняем переадресацию на корень веб-сайта (то есть на функцию index).
@login_required
@group_required("Managers")
def board_create(request):
    if request.method == "POST":
        board = Board()        
        board.name = request.POST.get("name")
        board.description = request.POST.get("description")
        board.save()
        return HttpResponseRedirect(reverse('board_index'))
    else:        
        boardform = BoardForm()
        return render(request, "board/create.html", {"form": boardform})

# Функция edit выполняет редактирование объекта.
# Функция в качестве параметра принимает идентификатор объекта в базе данных.
@login_required
@group_required("Managers")
def board_edit(request, id):
    try:
        board = Board.objects.get(id=id) 
        if request.method == "POST":
            board.name = request.POST.get("name")
            board.description = request.POST.get("description")
            board.save()
            return HttpResponseRedirect(reverse('board_index'))
        else:
            # Загрузка начальных данных
            boardform = BoardForm(initial={'name': board.name, 'description': board.description })
            return render(request, "board/edit.html", {"form": boardform})
    except Board.DoesNotExist:
        return HttpResponseNotFound("<h2>Board not found</h2>")

# Удаление данных из бд
# Функция delete аналогичным функции edit образом находит объет и выполняет его удаление.
@login_required
@group_required("Managers")
def board_delete(request, id):
    try:
        board = Board.objects.get(id=id)
        board.delete()
        return HttpResponseRedirect(reverse('board_index'))
    except Board.DoesNotExist:
        return HttpResponseNotFound("<h2>Board not found</h2>")

# Просмотр страницы read.html для просмотра объекта.
@login_required
def board_read(request, id):
    try:
        board = Board.objects.get(id=id) 
        return render(request, "board/read.html", {"board": board})
    except Board.DoesNotExist:
        return HttpResponseNotFound("<h2>Board not found</h2>")

@login_required
def new_topic(request, pk):
    board = get_object_or_404(Board, pk=pk)
    if request.method == 'POST':
        form = NewTopicForm(request.POST)
        if form.is_valid():
            topic = form.save(commit=False)
            topic.board = board
            topic.starter = request.user  # <- here
            topic.save()
            Post.objects.create(
                message=form.cleaned_data.get('message'),
                topic=topic,
                created_by=request.user  # <- and here
            )
            return redirect('topic_posts', pk=pk, topic_pk=topic.pk)  # <- here
            #return redirect('board_topics', pk=board.pk)  # TODO: redirect to the created topic page
    else:
        form = NewTopicForm()
    return render(request, 'forum/new_topic.html', {'board': board, 'form': form})

def topic_posts(request, pk, topic_pk):
    topic = get_object_or_404(Topic, board__pk=pk, pk=topic_pk)
    topic.views += 1
    topic.save()
    return render(request, 'forum/topic_posts.html', {'topic': topic})

@login_required
def reply_topic(request, pk, topic_pk):
    topic = get_object_or_404(Topic, board__pk=pk, pk=topic_pk)
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.topic = topic
            post.created_by = request.user
            post.save()

            topic.last_updated = timezone.now()  # <- здесь
            topic.save()                         # <- здесь

            return redirect('topic_posts', pk=pk, topic_pk=topic_pk)
    else:
        form = PostForm()
    return render(request, 'forum/reply_topic.html', {'topic': topic, 'form': form})

@method_decorator(login_required, name='dispatch')
class PostUpdateView(UpdateView):
    model = Post
    fields = ('message', )
    template_name = 'forum/edit_post.html'
    pk_url_kwarg = 'post_pk'
    context_object_name = 'post'
    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(created_by=self.request.user)
    def form_valid(self, form):
        post = form.save(commit=False)
        post.updated_by = self.request.user
        post.updated_at = timezone.now()
        post.save()
        return redirect('topic_posts', pk=post.topic.board.pk, topic_pk=post.topic.pk)    

class PostListView(ListView):
    model = Post
    context_object_name = 'posts'
    template_name = 'forum/topic_posts.html'
    paginate_by = 20
    def get_context_data(self, **kwargs):

        session_key = 'viewed_topic_{}'.format(self.topic.pk)  # <- здесь
        if not self.request.session.get(session_key, False):
            self.topic.views += 1
            self.topic.save()
            self.request.session[session_key] = True           # <- пока здесь

        kwargs['topic'] = self.topic
        return super().get_context_data(**kwargs)
    def get_queryset(self):
        self.topic = get_object_or_404(Topic, board__pk=self.kwargs.get('pk'), pk=self.kwargs.get('topic_pk'))
        queryset = self.topic.posts.order_by('created_at')
        return queryset

# Список для изменения с кнопками создать, изменить, удалить
@login_required
@group_required("Managers")
def news_index(request):
    #news = News.objects.all().order_by('surname', 'name', 'patronymic')
    #return render(request, "news/index.html", {"news": news})
    news = News.objects.all().order_by('-daten')
    return render(request, "news/index.html", {"news": news})

# Список для просмотра
def news_list(request):
    news = News.objects.all().order_by('-daten')
    return render(request, "news/list.html", {"news": news})

# В функции create() получаем данные из запроса типа POST, сохраняем данные с помощью метода save()
# и выполняем переадресацию на корень веб-сайта (то есть на функцию index).
@login_required
@group_required("Managers")
def news_create(request):
    if request.method == "POST":
        news = News()        
        news.daten = request.POST.get("daten")
        news.title = request.POST.get("title")
        news.details = request.POST.get("details")
        if 'photo' in request.FILES:                
            news.photo = request.FILES['photo']        
        news.save()
        return HttpResponseRedirect(reverse('news_index'))
    else:        
        #newsform = NewsForm(request.FILES, initial={'daten': datetime.datetime.now().strftime('%Y-%m-%d'),})
        newsform = NewsForm(initial={'daten': datetime.datetime.now().strftime('%Y-%m-%d'), })
        return render(request, "news/create.html", {"form": newsform})

# Функция edit выполняет редактирование объекта.
# Функция в качестве параметра принимает идентификатор объекта в базе данных.
@login_required
@group_required("Managers")
def news_edit(request, id):
    try:
        news = News.objects.get(id=id) 
        if request.method == "POST":
            news.daten = request.POST.get("daten")
            news.title = request.POST.get("title")
            news.details = request.POST.get("details")
            if "photo" in request.FILES:                
                news.photo = request.FILES["photo"]
            news.save()
            return HttpResponseRedirect(reverse('news_index'))
        else:
            # Загрузка начальных данных
            newsform = NewsForm(initial={'daten': news.daten.strftime('%Y-%m-%d'), 'title': news.title, 'details': news.details, 'photo': news.photo })
            return render(request, "news/edit.html", {"form": newsform})
    except News.DoesNotExist:
        return HttpResponseNotFound("<h2>News not found</h2>")

# Удаление данных из бд
# Функция delete аналогичным функции edit образом находит объет и выполняет его удаление.
@login_required
@group_required("Managers")
def news_delete(request, id):
    try:
        news = News.objects.get(id=id)
        news.delete()
        return HttpResponseRedirect(reverse('news_index'))
    except News.DoesNotExist:
        return HttpResponseNotFound("<h2>News not found</h2>")

# Просмотр страницы read.html для просмотра объекта.
@login_required
def news_read(request, id):
    try:
        news = News.objects.get(id=id) 
        return render(request, "news/read.html", {"news": news})
    except News.DoesNotExist:
        return HttpResponseNotFound("<h2>News not found</h2>")

# Регистрационная форма 
def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return HttpResponseRedirect(reverse('index'))
            #return render(request, 'registration/register_done.html', {'new_user': user})
    else:
        form = SignUpForm()
    return render(request, 'registration/signup.html', {'form': form})

# Изменение данных пользователя
@method_decorator(login_required, name='dispatch')
class UserUpdateView(UpdateView):
    model = User
    fields = ('first_name', 'last_name', 'email',)
    template_name = 'registration/my_account.html'
    success_url = reverse_lazy('index')
    #success_url = reverse_lazy('my_account')
    def get_object(self):
        return self.request.user




