import django_filters
from django.db import models

from .models import Post
from django import forms


class NewsFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(field_name='title', label='По заголовкам ')
    category__category_name = django_filters.CharFilter(label='По разделу ')
    type = django_filters.CharFilter(label='По типу ')
    date = django_filters.DateFilter(field_name='date', lookup_expr='gte', label='Дата написания от ',
                                     widget=forms.DateInput(attrs={
                                         'type': 'date',
                                         'id': 'start',
                                         'value': '2022-01-01',
                                         'min': '2021-01-01',
                                         'max': '2025-12-31'}))

    class Meta:
        model = Post
        fields = ['title', 'category__category_name', 'date', 'type']

        filter_overrides = {
            models.CharField: {
                'filter_class': django_filters.CharFilter,
                'extra': lambda f: {
                    'lookup_expr': 'icontains',
                },
            }
        }
