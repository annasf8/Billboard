import django_filters
from .models import Bill



class BillFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(lookup_expr='icontains', label='Title')

    class Meta:
        model = Bill
        fields = ['title']
