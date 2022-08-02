from django import forms
from django.core.exceptions import ValidationError
from django.forms import Textarea, SelectMultiple

from .models import Post, Category, Author, User


class PostForm(forms.ModelForm):
    author = forms.ModelChoiceField(queryset=Author.objects.all(),
                                    label='Автор поста',
                                    empty_label='-- Выберите автора --',)
    category = forms.ModelMultipleChoiceField(queryset=Category.objects.all(),
                                              label='Категория поста', widget=SelectMultiple(attrs={'multiple': True}))
    title = forms.CharField(min_length=15, max_length=150, label='Заголовок поста')
    text = forms.CharField(widget=Textarea(attrs={'cols': 80, 'rows': 10}), label='Текст поста', min_length=200)

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


class ArticleForm(forms.ModelForm):
    author = forms.ModelChoiceField(queryset=Author.objects.all(),
                                    label='Автор поста',
                                    empty_label='-- Выберите автора --',)
    category = forms.ModelMultipleChoiceField(queryset=Category.objects.all(),
                                              label='Категория поста', widget=SelectMultiple(attrs={'multiple': True}))
    title = forms.CharField(min_length=15, max_length=150, label='Заголовок поста')
    text = forms.CharField(widget=Textarea(attrs={'cols': 80, 'rows': 10}), label='Текст поста', min_length=200)

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