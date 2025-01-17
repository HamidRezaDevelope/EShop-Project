from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required

from django.http import HttpRequest , JsonResponse
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.urls import reverse
from django.views import View
from django.views.generic import TemplateView
from django.utils.decorators import method_decorator
from account_module.models import User
from order_module.models import Order, OrderDetails
from user_panel_module.forms import EditProfileModelForm, ChangePasswordForm



@method_decorator(login_required, name='dispatch')
class UserPanelDashboardPage(TemplateView):
    template_name = 'user_panel_module/user_panel_dashboard_page.html'


@method_decorator(login_required, name='dispatch')
class EditProfileView(View):
    def get(self,request:HttpRequest):
        current_user= User.objects.filter(id=request.user.id).first()
        edit_form = EditProfileModelForm(instance=current_user)
        context = {
            'form':edit_form
        }
        return render(request,'user_panel_module/edit_profile_page.html',context)
    def post(self, request:HttpRequest):
        current_user = User.objects.filter(id=request.user.id).first()
        edit_form= EditProfileModelForm(request.POST,request.FILES, instance=current_user)
        context = {
            'form': edit_form,
            'current_user' : current_user
        }
        edit_form.save(commit=True)
        return render(request,'user_panel_module/edit_profile_page.html',context)


@method_decorator(login_required, name='dispatch')
class ChangePasswordPage(View):
    def get(self,request: HttpRequest):
        form = ChangePasswordForm()
        context = {
            'form': form
        }
        return render(request,'user_panel_module/change_password_page.html',context)

    def post(self, request: HttpRequest):
        form = ChangePasswordForm(request.POST)
        if form.is_valid():
            current_user:User =User.objects.filter(id = request.user.id).first()
            if current_user.check_password(form.cleaned_data.get('current_password')):
                current_user.set_password(form.cleaned_data.get('password'))
                current_user.save()
                logout(request)
                return redirect(reverse ('login_page'))
            else:
                form.add_error('password','کلمه عبور و تکرار کلمه عبور مغایرت دارد')
        context = {
            'form':form
        }
        return render(request, 'user_panel_module/change_password_page.html', context)


@login_required()
def user_panel_menu_component(request):
    return render(request,'user_panel_module/components/user_panel_menu_components.html')

@login_required()
def user_basket(request: HttpRequest):
    current_order, created = Order.objects.prefetch_related('orderdetails_set').get_or_create(is_paid=False, user_id=request.user.id)
    total_amount = total_amount =current_order.calculate_total_price()
    # for order_detail in current_order.orderdetails_set.all():
    #     total_amount += order_detail.product.price * order_detail.count
    context = {
         'order' : current_order,
         'sum' : total_amount
    }
    return render(request,'user_panel_module/user_basket_page.html',context)


@login_required()
def remove_order_basket(request):
    detail_id = request.GET.get('detail_id')
    if detail_id is None:
        return JsonResponse({
            'status': 'detail_id_not_found'
        })
    current_order, created = Order.objects.prefetch_related('orderdetails_set').get_or_create(is_paid=False, user_id=request.user.id)
    detail = current_order.orderdetails_set.filter(id=detail_id).first()
    if detail is None:
        return JsonResponse({
            'status': 'detail_not_found'
        })
    detail.delete()
    current_order, created = Order.objects.prefetch_related('orderdetails_set').get_or_create(is_paid=False, user_id=request.user.id)

    total_amount =current_order.calculate_total_price()
    # for order_detail in current_order.orderdetails_set.all():
    #     total_amount += order_detail.product.price * order_detail.count
    context = {
        'order': current_order,
        'sum': total_amount
    }
    data = render_to_string('user_panel_module/remove_order_basket.html',context)
    return JsonResponse({
        'status': 'success',
        'body': data
    })


@login_required()
def change_order_detail_count(request : HttpRequest):
    detail_id = request.GET.get('detail_id')
    state = request.GET.get('state')
    if detail_id is None or state is None:
        return JsonResponse({
            'status' : 'detail_id_or_state_not_found'
        })
    order_detail= OrderDetails.objects.filter(id= detail_id, order__user_id= request.user.id, order__is_paid= False).first()
    if order_detail is None:
        return JsonResponse({
            'status': 'detail_not_found'
        })
    if state == 'increase':
        order_detail.count += 1
        order_detail.save()
    elif state == 'decrease':
        if order_detail.count == 1:
            order_detail.delete()
        else:
            order_detail.count -= 1
            order_detail.save()
    else:
        return JsonResponse({
            'status': 'state_invalid'
        })
    current_order, created = Order.objects.prefetch_related('orderdetails_set').get_or_create(is_paid=False,
                                                                                              user_id=request.user.id)

    total_amount = current_order.calculate_total_price()
    # for order_detail in current_order.orderdetails_set.all():
    #     total_amount += order_detail.product.price * order_detail.count
    context = {
        'order': current_order,
        'sum': total_amount
    }
    data = render_to_string('user_panel_module/user_basket_page.html', context)
    return JsonResponse({
        'status': 'success',
        'body': data
    })
