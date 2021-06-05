import django_filters
from django_filters import *
from .models import *

class ProductFilter(django_filters.FilterSet):
    price_filter = NumberFilter(field_name="price", lookup_expr='lt')
    name_filter = CharFilter(field_name="name", lookup_expr="icontains")
    class Meta:
        model = Product
        fields = "__all__"
        exclude = ['productCode', 'description', 'date_create', 'price', 'name']

class CategoryViewProductFilter(django_filters.FilterSet):
    price_filter = NumberFilter(field_name="price", lookup_expr='lt')
    name_filter = CharFilter(field_name="name", lookup_expr="icontains")
    class Meta:
        model = Product
        fields = "__all__"
        exclude = ["category", 'productCode', 'description', 'date_create', 'price', 'name']

class CustomerViewOrderItem(django_filters.FilterSet):
    class Meta:
        model = Order
        fields = "__all__"
        exclude = ["customer",]

class CategoryFilter(django_filters.FilterSet):
    name_filter = CharFilter(field_name="name", lookup_expr="icontains")
    productCode_filter = CharFilter(field_name="productCode", lookup_expr="icontains")
    price_filter = NumberFilter(field_name="price", lookup_expr='gte')
    date_start_filter = DateFilter(
        'start',
        # lookup_type='contains'
    )

    class Meta:
        model = Category
        fields = "__all__"
        exclude = (
            "category",
            "description",
            "date_created"
        )




class CustomerFilter(django_filters.FilterSet):
    name_filter = CharFilter(field_name="name", lookup_expr="icontains")
    phone_filter = CharFilter(field_name="phone", lookup_expr="icontains")
    email_filter = CharFilter(field_name="email", lookup_expr="icontains")
    class Meta:
        model = Customer
        fields = ()