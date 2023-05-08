import django_filters
from django_filters import CharFilter
from nemo.models import *
from django import forms


class CandidateFilter(django_filters.FilterSet):

    id = django_filters.NumberFilter(
        field_name='id',
        lookup_expr='icontains',
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )
    
    first_name = django_filters.CharFilter(
        field_name='first_name',
        lookup_expr='icontains',
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    
       
    class Meta:
        model = Candidate
        fields = ['id','first_name','rank', 'vessel_type','experience','license_country']


   
   
