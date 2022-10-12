import django_filters
from django.db import models
from django.utils.translation import gettext as _
from django.utils.translation import pgettext_lazy
from django import forms

from .models import Post, Category



class NewsFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(field_name='title',
                                      label=pgettext_lazy('text for NewsFilter', 'By title'),
                                      lookup_expr='icontains')
    category__category_name = django_filters.ModelMultipleChoiceFilter(queryset=Category.objects.all(),
                                                                       label=pgettext_lazy('text for NewsFilter', 'By category'),
                                                                       to_field_name='category_name')
    date = django_filters.DateFilter(field_name='date',
                                     lookup_expr='gte',
                                     label=pgettext_lazy('text for NewsFilter', 'Date of writing from'),
                                     widget=forms.DateInput(attrs={
                                         'type': 'date',
                                         'id': 'start',
                                         'value': '2022-01-01',
                                         'min': '2021-01-01',
                                         'max': '2025-12-31'}))

    class Meta:
        model = Post
        fields = ['title', 'category__category_name', 'date']
