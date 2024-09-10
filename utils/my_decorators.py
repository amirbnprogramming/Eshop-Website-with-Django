from django.http import HttpRequest
from django.shortcuts import redirect
from django.urls import reverse_lazy


def login_permission_checker_decorator_factory(data=None):
    def login_permission_checker_decorator(view_func):
        def wrapper(request: HttpRequest, *args, **kwargs):
            if request.user.is_authenticated and request.user.is_superuser:
                return view_func(request, *args, **kwargs)
            else:
                return redirect(reverse_lazy('login_page'))

        return wrapper

    return login_permission_checker_decorator
