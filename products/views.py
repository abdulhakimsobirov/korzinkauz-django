from django.shortcuts import render, redirect
from django.forms import inlineformset_factory
from django.contrib.auth import authenticate, login, logout
# from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.http import HttpResponse
from django.utils.translation import gettext as _
from django.template import RequestContext
from datetime import datetime

#
from .forms import *
from .filters import *
from .decorators import *

# Create your views here.

def home(request):
    context={
        'hello':_("Hello")
    }
    return render(request, 'products/home.html', context)
@logout_required
def register(request):    
    registered = False
    if request.method == "POST":
        user_form = UserForm(data=request.POST)
        customerForm = CustomerForm(data=request.POST)
        if len(request.POST['password']) == 0:
            messages.info(request, "Enter the password!")
        if len(request.POST['password']) < 8:
            messages.info(request, "Password min length 8")
        if user_form.is_valid() and customerForm.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            group = Group.objects.get(name='customer')
            user.groups.add(group)
            user.save()
            registered = True
            customer = customerForm.save(commit=False)
            customer.user = user
            customer.save()
        else:
            messages.info(request, user_form.errors)
    else:
        user_form = UserForm()
        customerForm = CustomerForm()
    return render(request, 'products/registration.html',
                    context={'user_form': user_form, "customerForm":customerForm, "registered": registered} )
    
@logout_required
def user_login(request):
    loginning = False
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                request.session['username'] = username

                loginning = True
                response = render(request, "products/login.html", {'username':username, 'loginning':loginning})
                response.set_cookie('last_connection', datetime.now())
                response.set_cookie('username', datetime.now())
                return response
        else:
            print("SOMEONE TRIED TO LOGIN and FIELD!")
            print(f"Username: {username} and password: {password}")
            messages.info(request, "Username OR Password is incurrent")
    if loginning:
        username = request.session['username']
    else:
        username = request.user
    # print(messages)
    return render(request, "products/login.html",
                    {'username':username})

@login_required
def user_logout(request):
    try:
        del request.session['username']
    except:
        pass
    logout(request)
    return redirect("/")


@login_required
def user_profile(request):
    # user = request.user
    # customer = Customer.objects.get(id=1)
    # userForm = UserForm(instance=user)
    # customerForm = CustomerForm(instance=customer)
    # orders = Order.objects.filter(customer=customer)
    # if request.method == "POST":
    #     userForm = UserForm(request.POST, instance=user)
    #     # customerForm = CustomerForm(data=request.POST, files=request.FILES, instance=customer)
    #     if userForm.is_valid():
    #         print(request.FILES)
    #         userForm.save()
    #         # customer = customerForm.save()
    #         return redirect("/user/")
    return render(request, 'products/user_profile.html',)# {'form': userForm})#, 'form2':customerForm, 'orders':orders})
@login_required
def userSetting(request):
    user = request.user
    customer = Customer.objects.get(id=1)
    userForm = ProfileForm(instance=user)
    customerForm = CustomerForm(instance=customer)
    orders = Order.objects.filter(customer=customer)
    if request.method == "POST":
        userForm = ProfileForm(request.POST, instance=user)
        customerForm = CustomerForm(data=request.POST, files=request.FILES, instance=customer)

        if customerForm.is_valid() and userForm.is_valid():
            print(request.FILES)
            userForm.save()
            customer = customerForm.save(commit=False)
            customer.user = request.user
            customer.save()
            return redirect("/user/")
        else:
            return HttpResponse("Error")
    return render(request, 'products/editProfile.html', {'form':userForm,'form2':customerForm, 'orders':orders})


@login_required
@admin_only
def categoryViewID(request, pk):
    category=Category.objects.get(id=pk)
    productS = Product.objects.filter(category=category)
    myFilter = CategoryViewProductFilter(request.GET, queryset=productS)
    productS = myFilter.qs
    my_dict = {"products": productS, "category":category, "productsLength":productS.count(),
    'myFilter':myFilter}
    return render(request, "products/view/categoryViewID.html", context=my_dict)

@login_required
@admin_only
def customerViewID(request, pk):
    customer=Customer.objects.get(id=pk)
    orderItem = Order.objects.filter(customer=customer)
    myFilter = CustomerViewOrderItem(request.GET, queryset=orderItem)
    orderItem = myFilter.qs
    my_dict = {"orderItem": orderItem, "customer":customer, "orderItemLength":orderItem.count(),
    'myFilter':myFilter}
    return render(request, "products/view/customerViewID.html", context=my_dict)





# Crud Product

@login_required
@allowed_users(['manager', 'admin'])
def products(request):
    productS = Product.objects.all()
    myFilter = ProductFilter(request.GET, queryset=productS)
    productS = myFilter.qs
    my_dict = {"products": productS,
    "myFilter":myFilter}
    return render(request, "products/products.html", context=my_dict)

@login_required
@admin_only
def createProduct(request):
    if request.method == "POST":
        productFrom = ProductForm(data=request.POST)
        print(request.POST)
        if productFrom.is_valid():
            productFrom.save(commit=True)
            return redirect("/product/")
    else:
        productFrom = ProductForm()

    return render(request, "products/create/createProduct.html", context={
            "form": productFrom,
        })

@login_required
@admin_only
def createProductToCategory(request, pk):
    MyFormSet = inlineformset_factory(Category, Product, 
        fields=("name", "productCode", 'price'), extra=5
    )
    category = Category.objects.get(id=pk)
    formset = MyFormSet(queryset=Product.objects.none(), instance=category)

    print(category)

    if request.method == "POST":
        formset = MyFormSet(request.POST, instance=category)
        print(request.POST)
        if formset.is_valid():
            formset.save()
            return redirect(f"/category/{pk}")

    return render(request, "products/create/createProductSet.html", context={
            "formset": formset,
        })

@login_required
@admin_only
def updateProduct(request, pk):
    product = Product.objects.get(id=pk)
    if request.method == "POST":
        productForm = ProductForm(data=request.POST, instance=product)
        if productForm.is_valid():
            productForm.save()
            return redirect("/product/")
    else:
        productForm = ProductForm(instance=product)

    return render(request, "products/update/updateProduct.html", context={
            "form": productForm,
        })

@login_required
@admin_only
def deleteProduct(request, pk):
    product = Product.objects.get(id=pk)
    if request.method == 'POST':
        product.delete()
        return redirect('/product/')
    return render(request, 'products/delete/deleteProduct.html', context={'item':product})

# Crud Category
@login_required
@allowed_users(['manager', 'admin'])
def category(request):
    category = Category.objects.all()
    myFilter = CategoryFilter(request.GET, queryset=category)
    category = myFilter.qs

    my_dict = {"categorys": category, "myFilter":myFilter}
    return render(request, "products/category.html",
                  context=my_dict)


@login_required
@admin_only
def createCategory(request):
    if request.method == "POST":
        categoryForm = CategoryForm(data=request.POST)
        print(request.POST)
        if categoryForm.is_valid():
            categoryForm.save()
            return redirect("/category/")
    else:
        categoryForm = CategoryForm()

    return render(request, "products/create/createCategory.html", context={
            "form": categoryForm,
        })

@login_required
@admin_only
def updateCategory(request, pk):
    category = Category.objects.get(id=pk)
    if request.method == "POST":
        categoryForm = CategoryForm(data=request.POST, instance=category)
        if categoryForm.is_valid():
            categoryForm.save()
            return redirect("/category/")
    else:
        categoryForm = CategoryForm(instance=category)

    return render(request, "products/update/updateCategory.html", context={
            "form": categoryForm,
        })

@login_required
@admin_only
def deleteCategory(request, pk):
    category = Category.objects.get(id=pk)
    if request.method == 'POST':
        category.delete()
        return redirect('/category/')
    return render(request, 'products/delete/deleteCategory.html', context={'item':category})

#Crud Customer
@login_required
@allowed_users(['manager', 'admin'])
def customer(request):
    customers = Customer.objects.all()
    myFilter = CustomerFilter(request.GET, queryset=customers)
    customers = myFilter.qs

    my_dict = {"customers": customers, "myFilter":myFilter}
    
    return render(request, "products/customer.html",
                  context=my_dict)

@login_required
@admin_only
def createCustomer(request):
    if request.method == "POST":
        customerForm = CustomerForm(data=request.POST)
        print(request.POST)
        if customerForm.is_valid():
            customerForm.save()
            return redirect("/customer/")
    else:
        customerForm = CustomerForm()

    return render(request, "products/create/createCustomer.html", context={
            "form": customerForm,
        })

@login_required
@admin_only
def createOrderItemToCustomer(request, pk):
    MyFormSet = inlineformset_factory(Customer, Order, 
        fields=(
            "orderCode",
            "status",
            "customer",
            "products",
        ), extra=5
    )
    customer = Customer.objects.get(id=pk)
    print(Customer.objects.last().id)
    formset = MyFormSet(queryset=Order.objects.none(), instance=customer)
    
    if request.method == "POST":
        formset = MyFormSet(request.POST, instance=customer)
        print(request.POST)
        if formset.is_valid():
            formset.save()
            return redirect(f"/customer/{pk}")

    return render(request, "products/create/createOrderSet.html", context={
            "formset": formset,
        })

@login_required
@admin_only
def updateCustomer(request, pk):
    customer = Customer.objects.get(id=pk)
    if request.method == "POST":
        customerForm = CustomerForm(data=request.POST, instance=customer)
        if customerForm.is_valid():
            customerForm.save()
            return redirect("/customer/")
    else:
        customerForm = CustomerForm(instance=customer)

    return render(request, "products/update/updateCustomer.html", context={
            "form": customerForm,
        })

@login_required
@admin_only
def deleteCustomer(request, pk):

    customer = Customer.objects.get(id=pk)
    if request.method == 'POST':
        customer.delete()
        return redirect('/customer/')
    return render(request, 'products/delete/deleteCustomer.html', context={'item':customer})

#Crud Status
@login_required
@allowed_users(['manager', 'admin'])
def status(request):
    my_dict = {"status": Status.objects.all(),}

    return render(request, "products/status.html",
                  context=my_dict)

@login_required
@admin_only
def createStatus(request):
    if request.method == "POST":
        statusForm = StatusForm(data=request.POST)
        print(request.POST)
        if statusForm.is_valid():
            statusForm.save(commit=True)
            return redirect("/status/")
    else:
        statusForm = StatusForm()

    return render(request, "products/create/createStatus.html", context={
            "form": statusForm,
        })

@login_required
@admin_only
def updateStatus(request, pk):
    status = Status.objects.get(id=pk)
    if request.method == "POST":
        statusForm = StatusForm(data=request.POST, instance=status)
        if statusForm.is_valid():
            statusForm.save()
            return redirect("/status/")
    else:
        statusForm = StatusForm(instance=status)

    return render(request, "products/update/updateStatus.html", context={
            "form": statusForm,
        })

@login_required
@admin_only
def deleteStatus(request, pk):
    status = Status.objects.get(id=pk)
    if request.method == 'POST':
        status.delete()
        return redirect('/status/')
    return render(request, 'products/delete/deleteStatus.html', context={'item':status})

# Crud Order
@login_required
@allowed_users(['manager', 'admin'])
def order(request):
    my_dict = {"orders": Order.objects.all(),}

    return render(request, "products/order.html",
                  context=my_dict)

@login_required
@admin_only
def createOrder(request):
    if request.method == "POST":
        orderForm = OrderForm(data=request.POST)
        if orderForm.is_valid:
            orderForm.save()
            return redirect("/order/")
    else:
        orderForm = OrderForm()

    return render(request, "products/create/createOrder.html", context={
            "form": orderForm,
        })


@login_required
@admin_only
def updateOrder(request, pk):
    order = Order.objects.get(id=pk)
    if request.method == "POST":
        orderForm = OrderForm(data=request.POST, instance=order)
        if orderForm.is_valid():
            orderForm.save()
            return redirect("/order/")
    else:
        orderForm = OrderForm(instance=order)

    return render(request, "products/update/updateOrder.html", context={
            "form": orderForm,
        })

@login_required
@admin_only
def deleteOrder(request, pk):
    order = Order.objects.get(id=pk)
    if request.method == 'POST':
        order.delete()
        return redirect('/order/')

    return render(request, 'products/delete/deleteOrder.html', context={'item':order})


