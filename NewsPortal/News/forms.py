from django.core.exceptions import ValidationError
from django.forms import Textarea, SelectMultiple
from django.contrib.auth.models import Group
from allauth.account.forms import SignupForm
from django import forms

from .models import Post, Category, Author, User


class PostForm(forms.ModelForm):
    author = forms.ModelChoiceField(queryset=Author.objects.all(),
                                    label='Автор поста',
                                    empty_label='-- Выберите автора --', )
    category = forms.ModelMultipleChoiceField(queryset=Category.objects.all(),
                                              label='Категория поста', widget=SelectMultiple(attrs={'multiple': True}))
    title = forms.CharField(min_length=15, max_length=150, label='Заголовок поста')
    text = forms.CharField(widget=Textarea(attrs={'cols': 80, 'rows': 10}), label='Текст поста', min_length=100)

    class Meta:
        model = Post
        fields = [
            'author',
            'category',
            'title',
            'text',
        ]

    def clean(self):
        clean_data = super().clean()
        title = clean_data.get('title')
        text = clean_data.get('text')
        if title == text:
            raise ValidationError('Текст поста не должен быть идентичен заголовку.')
        return clean_data


class ArticleForm(forms.ModelForm):
    author = forms.ModelChoiceField(queryset=Author.objects.all(),
                                    label='Автор поста',
                                    empty_label='-- Выберите автора --', )
    category = forms.ModelMultipleChoiceField(queryset=Category.objects.all(),
                                              label='Категория поста', widget=SelectMultiple(attrs={'multiple': True}))
    title = forms.CharField(min_length=15, max_length=150, label='Заголовок поста')
    text = forms.CharField(widget=Textarea(attrs={'cols': 80, 'rows': 10}), label='Текст поста', min_length=100)

    class Meta:
        model = Post
        fields = [
            'author',
            'category',
            'title',
            'text',
        ]

    def clean(self):
        clean_data = super().clean()
        title = clean_data.get('title')
        text = clean_data.get('text')
        if title == text:
            raise ValidationError('Текст поста не должен быть идетичен заголовку.')
        return clean_data


class ProfileForm(forms.ModelForm):
    class Meta:
        username = forms.CharField(label='Имя пользователя')
        first_name = forms.CharField(label='Имя')
        last_name = forms.CharField(label='Фамилия')
        email = forms.EmailField(label='Электронная почта')

        model = User
        fields = [
            'username',
            'first_name',
            'last_name',
            'email',
        ]


class BasicSignupForm(SignupForm):

    def save(self, request):
        user = super(BasicSignupForm, self).save(request)
        basic_group = Group.objects.get(name='common')
        basic_group.user_set.add(user)
        return user


class MyCustomSocialSignupForm(SignupForm):
    def save(self, request):
        user = super(MyCustomSocialSignupForm, self).save(request)
        basic_group = Group.objects.get(name='common')
        basic_group.user_set.add(user)
        return user
