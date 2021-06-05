from django.urls import path
from django.http import JsonResponse
from .views import *

def api_urls(request):
     urls_arr = [
        '/api/',
        '/api/product/',
        '/api/product/<int:pk>/',
        '/api/product/create/',
        '/api/product/update/<int:pk>/',
        '/api/product/delete/<int:pk>/',
        '/api/category/',
        '/api/category/<int:pk>/',
        '/api/category/create/',
        '/api/category/update/<int:pk>/',
        '/api/category/delete/<int:pk>/',
        '/api/customer/',
        '/api/customer/<int:pk>/',
        '/api/customer/create/',
        '/api/customer/update/<int:pk>/',
        '/api/customer/delete/<int:pk>/',
        '/api/status/',
        '/api/status/<int:pk>/',
        '/api/status/create/',
        '/api/status/update/<int:pk>/',
        '/api/status/delete/<int:pk>/',
        '/api/order/',
        '/api/order/<int:pk>/',
        '/api/order/create/',
        '/api/order/update/<int:pk>/',
        '/api/order/delete/<int:pk>/'
     ]
     urls = {}
     i = 0
     for item in urls_arr:
         i+=1
         urls[i] = item
     return JsonResponse(urls)

app_name = "api"
urlpatterns = [

]

off = ['''path('', api_urls, name="api_urls"),
    path('product/', products_API, name="products"),
    path('product/<int:pk>/', product_API, name="product"),
    path('product/create/', product_create_API, name="productCreate"),
    path('product/update/<int:pk>/', product_update_API, name="productUpdate"),
    path('product/delete/<int:pk>/', product_delete_API, name="productDelete"),

    path('category/', categorys_API, name="categorys"),
    path('category/<int:pk>/', category_API, name="category"),
    path('category/create/', category_create_API, name="categoryCreate"),
    path('category/update/<int:pk>/', category_update_API, name="categoryUpdate"),
    path('category/delete/<int:pk>/', category_delete_API, name="categoryDelete"),

    path('customer/', customers_API, name="categorys"),
    path('customer/<int:pk>/', customer_API, name="category"),
    path('customer/create/', customer_create_API, name="categoryCreate"),
    path('customer/update/<int:pk>/', customer_update_API, name="categoryUpdate"),
    path('customer/delete/<int:pk>/', customer_delete_API, name="categoryDelete"),

    path('status/', statuses_API, name="categorys"),
    path('status/<int:pk>/', status_API, name="category"),
    path('status/create/', status_create_API, name="categoryCreate"),
    path('status/update/<int:pk>/', status_update_API, name="categoryUpdate"),
    path('status/delete/<int:pk>/', status_delete_API, name="categoryDelete"),

    path('order/', orders_API, name="categorys"),
    path('order/<int:pk>/', order_API, name="category"),
    path('order/create/', order_create_API, name="categoryCreate"),
    path('order/update/<int:pk>/', order_update_API, name="categoryUpdate"),
    path('order/delete/<int:pk>/', order_delete_API, name="categoryDelete"),
''']