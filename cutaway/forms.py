from django import forms
from django.forms import ModelForm, TextInput, Textarea, DateInput, DateTimeInput, NumberInput, CheckboxInput
from .models import Message, Board, Topic, Post, News
#from django.utils.translation import ugettext as _
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

# При разработке приложения, использующего базу данных, чаще всего необходимо работать с формами, которые аналогичны моделям.
# В этом случае явное определение полей формы будет дублировать код, так как все поля уже описаны в модели.
# По этой причине Django предоставляет вспомогательный класс, который позволит вам создать класс Form по имеющейся модели
# атрибут fields - указание списка используемых полей, при fields = '__all__' - все поля
# атрибут widgets для указания собственный виджет для поля. Его значением должен быть словарь, ключами которого являются имена полей, а значениями — классы или экземпляры виджетов.

class BoardForm(forms.ModelForm):
    class Meta:
        model = Board
        fields = ('name', 'description')
        widgets = {
            'name': TextInput(attrs={"size":"100"}),
            'description': Textarea(attrs={'cols': 100, 'rows': 10}),                        
        }

class NewTopicForm(forms.ModelForm):
    message = forms.CharField(
        widget=forms.Textarea(
            attrs={'rows': 5, 'placeholder': 'What is on your mind?'}
        ),
        max_length=4000,
        help_text='The max length of the text is 4000.'
    )
    class Meta:
        model = Topic
        fields = ['subject', 'message']

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['message', ]

class NewsForm(forms.ModelForm):
    class Meta:
        model = News
        fields = ('daten', 'title', 'details', 'photo')
        widgets = {
            'dater': DateTimeInput(format='%d/%m/%Y %H:%M:%S'),
            'title': TextInput(attrs={"size":"100"}),
            'details': Textarea(attrs={'cols': 100, 'rows': 10}),                        
        }

# Форма регистрации
class SignUpForm(UserCreationForm):
    email = forms.CharField(max_length=254, required=True, widget=forms.EmailInput())
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
