from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render, get_object_or_404
from django.views.decorators.csrf import csrf_exempt

from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.viewsets import *
from rest_framework import status


from products.models import *
from .serializers import *
from .pagination import *

# viewset : list, create, retrive, update, protial_update, destory

class ProductsViewSet(ViewSet):
    def list(self, request):
        queryset = Product.objects.all()
        serializer = ProductSerializer(queryset, many=True)
        return Response(serializer.data)
    def post(self, request):
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        queryset = Product.objects.all()
        product = get_object_or_404(queryset, pk=pk)
        print(product)
        serializer = ProductSerializer(product)
        return Response(serializer.data)

# class ProductsViewSet(ModelViewSet):
#     queryset = Product.objects.all()
#     serializer_class = ProductSerializer
#     pagination_class = CustomPagination


"""
def object_or_404(model, pk):
    try:
        return model.objects.get(id=pk)
    except:
        return None


@api_view(['GET'])
def products_API(request):
    products = Product.objects.all()
    serializer = ProductSerializer(products, many=True)
    return JsonResponse(serializer.data, safe=False)

@api_view(['GET'])
def product_API(request, pk):
    product = object_or_404(Product, pk)
    if product:
        serializer = ProductSerializer(product, many=False)
        return JsonResponse(serializer.data, safe=False)
    else:
        return HttpResponse("The information in the id you provided is not available")

@csrf_exempt
@api_view(['POST'])
def product_create_API(request):
    serializer = ProductSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
    
    return JsonResponse(serializer.data)

@csrf_exempt
@api_view(['POST'])
def product_update_API(request, pk):
    product = object_or_404(Product, pk)
    if product:
        serializer = ProductSerializer(instance=product, data=request.data)
        if serializer.is_valid():
            serializer.save()
        return JsonResponse(serializer.data)
    else:
        return HttpResponse("The information in the id you provided is not available")

@csrf_exempt
@api_view(['DELETE'])
def product_delete_API(request, pk):
    product = object_or_404(Product, pk)
    if product:
        product.delete()
        return JsonResponse({"deleted product":True})
    else:
        return HttpResponse("The information in the id you provided is not available")
        
@api_view(['GET'])
def categorys_API(request):
    category = Category.objects.all()
    serializer = CategorySerializer(category, many=True)
    return JsonResponse(serializer.data, safe=False)

@api_view(['GET'])
def category_API(request, pk):
    category = object_or_404(Category, pk)
    if category:
        serializer = CategorySerializer(category, many=False)
        return JsonResponse(serializer.data, safe=False)
    else:
        return HttpResponse("The information in the id you provided is not available")

@csrf_exempt
@api_view(['POST'])
def category_create_API(request):
    serializer = CategorySerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
    
    return JsonResponse(serializer.data)

@csrf_exempt
@api_view(['POST'])
def category_update_API(request, pk):
    category = object_or_404(Category, pk)
    if category:
        serializer = CategorySerializer(instance=category, data=request.data)
        if serializer.is_valid():
            serializer.save()
        return JsonResponse(serializer.data)
    else:
        return HttpResponse("The information in the id you provided is not available")

@csrf_exempt
@api_view(['DELETE'])
def category_delete_API(request, pk):
    category = object_or_404(Category, pk)
    if category:
        category.delete()
        return JsonResponse({"deleted category":True})
    else:
        return HttpResponse("The information in the id you provided is not available")
        
@api_view(['GET'])
def customers_API(request):
    customers = Customer.objects.all()
    serializer = CustomerSerializer(customers, many=True)
    return JsonResponse(serializer.data, safe=False)

@api_view(['GET'])
def customer_API(request, pk):
    customer = object_or_404(Customer, pk)
    if customer:
        serializer = CustomerSerializer(customer, many=False)
        return JsonResponse(serializer.data, safe=False)
    else:
        return HttpResponse("The information in the id you provided is not available")

@csrf_exempt
@api_view(['POST'])
def customer_create_API(request):
    serializer = CustomerSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
    
    return JsonResponse(serializer.data)

@csrf_exempt
@api_view(['POST'])
def customer_update_API(request, pk):
    customer = object_or_404(Customer, pk)
    if customer:
        serializer = CustomerSerializer(instance=customer, data=request.data)
        if serializer.is_valid():
            serializer.save()
        return JsonResponse(serializer.data)
    else:
        return HttpResponse("The information in the id you provided is not available")

@csrf_exempt
@api_view(['DELETE'])
def customer_delete_API(request, pk):
    customer = object_or_404(Customer, pk)
    if customer:
        customer.delete()
        return JsonResponse({"deleted customer":True})
    else:
        return HttpResponse("The information in the id you provided is not available")
        
@api_view(['GET'])
def statuses_API(request):
    statuses = Status.objects.all()
    serializer = StatusSerializer(statuses, many=True)
    return JsonResponse(serializer.data, safe=False)

@api_view(['GET'])
def status_API(request, pk): 
    status = object_or_404(Status, pk)
    if status:
        serializer = StatusSerializer(status, many=False)
        return JsonResponse(serializer.data, safe=False)
    else:
        return HttpResponse("The information in the id you provided is not available")

@csrf_exempt
@api_view(['POST'])
def status_create_API(request):
    serializer = StatusSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
    
    return JsonResponse(serializer.data)

@csrf_exempt
@api_view(['POST'])
def status_update_API(request, pk):
    status = object_or_404(Status, pk)
    if status:
        serializer = StatusSerializer(instance=status, data=request.data)
        if serializer.is_valid():
            serializer.save()
        return JsonResponse(serializer.data)
    else:
        return HttpResponse("The information in the id you provided is not available")

@csrf_exempt
@api_view(['DELETE'])
def status_delete_API(request, pk):
    status = object_or_404(Status, pk)
    if status:
        status.delete()
        return JsonResponse({"deleted status":True})
    else:
        return HttpResponse("The information in the id you provided is not available")
        
@api_view(['GET'])
def orders_API(request):
    orders = Order.objects.all()
    serializer = OrderSerializer(orders, many=True)
    return JsonResponse(serializer.data, safe=False)

@api_view(['GET'])
def order_API(request, pk):
    order = object_or_404(Order, pk)
    if order:
        serializer = StatusSerializer(order, many=False)
        return JsonResponse(serializer.data, safe=False)
    else:
        return HttpResponse("The information in the id you provided is not available")

@csrf_exempt
@api_view(['POST'])
def order_create_API(request):
    serializer = StatusSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
    
    return JsonResponse(serializer.data)

@csrf_exempt
@api_view(['POST'])
def order_update_API(request, pk):
    order = object_or_404(Order, pk)
    if order:
        serializer = StatusSerializer(instance=order, data=request.data)
        if serializer.is_valid():
            serializer.save()
        return JsonResponse(serializer.data)
    else:
        return HttpResponse("The information in the id you provided is not available")

@csrf_exempt
@api_view(['DELETE'])
def order_delete_API(request, pk):
    order = object_or_404(Order, pk)
    if order:
        order.delete()
        return JsonResponse({"deleted order":True})
    else:
        return HttpResponse("The information in the id you provided is not available")
"""



