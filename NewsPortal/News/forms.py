from django.core.exceptions import ValidationError
from django.forms import Textarea, SelectMultiple
from django.contrib.auth.models import Group
from allauth.account.forms import SignupForm
from django import forms
from django.utils.translation import gettext as _
from django.utils.translation import pgettext_lazy

from .models import (
    Post,
    Category,
    Author,
    User,
    Comment,
)


class PostForm(forms.ModelForm):
    '''Форма поста(новости)'''
    author = forms.ModelChoiceField(queryset=Author.objects.all(),
                                    label=_('Author of post'),
                                    empty_label=_('-- choose author --'), )
    category = forms.ModelMultipleChoiceField(queryset=Category.objects.all(),
                                              label=_('Category of post'),
                                              widget=SelectMultiple(attrs={'multiple': True}))
    title = forms.CharField(min_length=15, max_length=150, label=_('Title of post'))
    text = forms.CharField(widget=Textarea(attrs={'cols': 80, 'rows': 10}),
                           label=pgettext_lazy('text for PostForm', 'Text'),
                           min_length=100)

    class Meta:
        model = Post
        fields = [
            'author',
            'category',
            'title',
            'text',
        ]

    def clean(self):
        '''Валидация формы: текст поста не должен совпадать с заголовком'''
        clean_data = super().clean()
        title = clean_data.get('title')
        text = clean_data.get('text')
        if title == text:
            raise ValidationError('Текст поста не должен быть идентичен заголовку.')
        return clean_data


class ArticleForm(forms.ModelForm):
    '''Форма поста(статьи)'''
    author = forms.ModelChoiceField(queryset=Author.objects.all(),
                                    label='Автор поста',
                                    empty_label='-- Выберите автора --', )
    category = forms.ModelMultipleChoiceField(queryset=Category.objects.all(),
                                              label='Категория поста',
                                              widget=SelectMultiple(attrs={'multiple': True}))
    title = forms.CharField(min_length=15, max_length=150, label='Заголовок поста')
    text = forms.CharField(widget=Textarea(attrs={'cols': 80, 'rows': 10}),
                           label='Текст поста',
                           min_length=100)

    class Meta:
        model = Post
        fields = [
            'author',
            'category',
            'title',
            'text',
        ]

    def clean(self):
        '''Валидация формы: текст поста не должен совпадать с заголовком'''
        clean_data = super().clean()
        title = clean_data.get('title')
        text = clean_data.get('text')
        if title == text:
            raise ValidationError('Текст поста не должен быть идетичен заголовку.')
        return clean_data


class ProfileForm(forms.ModelForm):
    '''Форма профиля пользовтеля '''

    class Meta:
        username = forms.CharField(label=_('Username'))
        first_name = forms.CharField(label=_('First name'))
        last_name = forms.CharField(label=_('Last name'))
        email = forms.EmailField(label=_('Email'))

        model = User
        fields = [
            'username',
            'first_name',
            'last_name',
            'email',
        ]


class BasicSignupForm(SignupForm):

    def save(self, request):
        '''При регистрации нового пользователя он добавляется в группу common'''
        user = super(BasicSignupForm, self).save(request)
        basic_group = Group.objects.get(name='common')
        basic_group.user_set.add(user)
        return user


class MyCustomSocialSignupForm(SignupForm):
    def save(self, request):
        '''При регистрации нового пользователя он добавляется в группу common'''
        user = super(MyCustomSocialSignupForm, self).save(request)
        basic_group = Group.objects.get(name='common')
        basic_group.user_set.add(user)
        return user


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('comment_text', 'user')
