from django.http import HttpResponse
from django.shortcuts import redirect, render


def get_ip(request):
    try:
        x_forward = request.META.get("HTTP_X_FORWARDED_FOR")
        if x_forward:
            ip1 = x_forward.split(",")[0]
        else:
            ip1 = request.META.get("REMOTE_ADDR")
    except:
        ip1 = ""
    return ip1

def logout_required(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('/')
        else:
            return view_func(request, *args, **kwargs)
    return wrapper_func

def login_required(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            return view_func(request, *args, **kwargs)
        else:
            return redirect("/")
    return wrapper_func


def allowed_users(allowed_roles=[]):
    def decorator(view_func):
        def wrapper_func(request, *args, **kwargs):
            group = None
            if request.user.groups.exists():
                group = request.user.groups.all()[0].name

            if group in allowed_roles:
                return view_func(request, *args, **kwargs)
            else:
                return render(request, '404.html')
        return wrapper_func
    return decorator

def admin_only(view_func):
    def wrapper_func(request, *args, **kwargs):
        group = None
        if request.user.groups.exists():
            group = request.user.groups.all()[0].name
        print(request.user, group)
        if group == "customer":
            return redirect("/")
        elif group == "manager":
            return redirect("/")
        elif group == "admin":
            return view_func(request, *args, **kwargs)
        else:
            return render(request, '404.html')
    return wrapper_func