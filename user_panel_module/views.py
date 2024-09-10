import encodings

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpRequest, JsonResponse
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic import TemplateView, ListView
from django.contrib.auth import login, logout

from account_module.models import User
from order_module.models import Order, OrderDetail
from product_module.models import Product
from user_panel_module.forms import UserEditProfileModelForm, UserEditPasswordForm


# Create your views here.
@method_decorator(login_required, name='dispatch')
class UserPanelDashboardPage(TemplateView):
    template_name = 'user_panel_module/user_panel_dashboard_page.html'


@method_decorator(login_required, name='dispatch')
class UserPastCartsPage(ListView):
    model = Order
    template_name = 'user_panel_module/user_past_carts.html'

    def get_queryset(self):
        current_user = self.request.user
        queryset = super().get_queryset()
        queryset = queryset.filter(user_id=current_user.id, is_paid=True).all()
        return queryset


@method_decorator(login_required, name='dispatch')
class UserEditProfilePage(View):
    def get(self, request):
        current_user = User.objects.filter(id=request.user.id).first()
        edit_form = UserEditProfileModelForm(instance=current_user)
        context = {
            'edit_form': edit_form,
            'current_user': current_user,
        }
        return render(request, 'user_panel_module/user_edit_profile.html', context)

    def post(self, request):
        current_user = User.objects.filter(id=request.user.id).first()
        edit_form = UserEditProfileModelForm(request.POST, request.FILES, instance=current_user)
        if edit_form.is_valid():
            edit_form.save(commit=True)
        context = {
            'edit_form': edit_form,
            'current_user': current_user,
        }
        return render(request, 'user_panel_module/user_edit_profile.html', context)


@method_decorator(login_required, name='dispatch')
class UserEditPasswordPage(View):
    def get(self, request):
        edit_password_form = UserEditPasswordForm()
        context = {
            'edit_password_form': edit_password_form,
        }
        return render(request, 'user_panel_module/user_edit_password.html', context)

    def post(self, request):
        edit_password_form = UserEditPasswordForm(request.POST)
        if edit_password_form.is_valid():
            current_user: User = User.objects.filter(id=request.user.id).first()
            if current_user.check_password(edit_password_form.cleaned_data.get('current_password')):
                current_user.set_password(edit_password_form.cleaned_data.get('new_password'))
                current_user.save()
                logout(request)
                return redirect(reverse('login_page'))
            else:
                edit_password_form.add_error('current_password', 'کلمه عبور وارد شده صحیح نمیباشد')

        context = {
            'edit_password_form': edit_password_form,
        }
        return render(request, 'user_panel_module/user_edit_password.html', context)


@login_required
def user_panel_menu_component(request):
    return render(request, 'user_panel_module/components/user_panel_menu_component.html', {})


@login_required
def user_cart(request: HttpRequest):
    current_user_id = request.user.id
    current_order, created = Order.objects.prefetch_related('orderdetail_set').get_or_create(user_id=current_user_id,
                                                                                             is_paid=False)
    total_price = current_order.get_order_total_price()
    context = {
        'order': current_order,
        'sum': total_price,
        'tax': total_price * 0.05,

    }
    print(context['tax'])

    return render(request, 'user_panel_module/user_cart_page.html', context)


@login_required
def remove_order_detail(request: HttpRequest):
    current_user_id = request.user.id
    selected_product_id = request.GET.get('selected_product_id')
    if selected_product_id is None:
        return JsonResponse({
            'status': 'selected_product_id_not_found'
        })

    else:
        # delete method return 2 important value
        deleted_count, deleted_dict = OrderDetail.objects.filter(id=selected_product_id, order__is_paid=False,
                                                                 order__user_id=current_user_id).delete()

        if deleted_count == 0:
            return JsonResponse({
                'status': 'selected_product_not_found'
            })

    current_order, created = Order.objects.prefetch_related('orderdetail_set').get_or_create(
        user_id=current_user_id, is_paid=False)
    total_price = current_order.get_order_total_price()

    context = {
        'order': current_order,
        'sum': total_price,
        'tax': total_price * 0.05,
    }
    print(context['tax'])
    returned_data = render_to_string('user_panel_module/user_cart_content.html', context)
    return JsonResponse({
        'status': 'success',
        'data': returned_data,
    })


@login_required
def change_order_detail_count(request):
    current_user_id = request.user.id
    selected_product_id = request.GET.get('selected_product_id')
    state = request.GET.get('state')
    if selected_product_id is None or state is None:
        return JsonResponse({
            'status': 'selected_product_id_not_found'
        })

    selected_product: OrderDetail = OrderDetail.objects.get(id=selected_product_id, order__user_id=current_user_id,
                                                            order__is_paid=False)

    if selected_product is None:
        return JsonResponse({
            'status': 'selected_product_not_found'
        })
    if state == 'increase':
        selected_product.count += 1
        selected_product.save()


    elif state == 'decrease':
        if selected_product.count == 1:
            selected_product.delete()

        else:
            selected_product.count -= 1
            selected_product.save()


    else:
        return JsonResponse({
            'status': 'state_invalid'
        })

    current_order, created = Order.objects.prefetch_related('orderdetail_set').get_or_create(
        user_id=current_user_id, is_paid=False)
    total_price = current_order.get_order_total_price()

    context = {
        'order': current_order,
        'sum': total_price,
        'tax': total_price * 0.05,

    }
    returned_data = render_to_string('user_panel_module/user_cart_content.html', context)
    return JsonResponse({
        'status': 'success',
        'data': returned_data,
    })


@login_required
def user_paid_factor_detail(request, order_id):
    current_user_id = request.user.id
    current_order_id = order_id
    current_order = Order.objects.prefetch_related('orderdetail_set').filter(id=order_id, user_id=current_user_id).first()
    if current_order is None:
        return JsonResponse({
            'status': 'order not found'
        })
    context = {
        'order': current_order,
    }
    return render(request, 'user_panel_module/user_past_carts_detail.html', context)
