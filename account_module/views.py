
from django.contrib.auth import get_user_model, login,logout
from django.core.mail import send_mail
from django.http import Http404
from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils.crypto import get_random_string
from django.views import View
from django.conf import settings

from account_module.forms import RegisterForm, LoginForm, ForgotPassForm, ResetPassForm
from account_module.models import User


# Create your views here.
user = get_user_model()
class RegisterView(View):
    def get(self,request):
        register_form = RegisterForm
        context = {
            'register_form' : register_form
        }
        return render(request,'account_module/register.html',context)

    def post(self,request):
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            User_email= register_form.cleaned_data.get('email')
            User_password= register_form.cleaned_data.get('password')
            user: bool = User.objects.filter(email__iexact=User_email).exists()
            if user:
                register_form.add_error('email','ایمیل تکراری است')
            else:
                new_user = User(email= User_email,email_active_code= get_random_string(72),
                                username = User_email,
                                is_active=False)
                new_user.set_password(User_password)
                new_user.save()
                send_mail('فعالسازی حساب کاربری','پیام ارسال ایمیل',recipient_list=[new_user.email],from_email=settings.EMAIL_HOST_USER)
                return redirect(reverse('login_page'))

        context = {
            'register_form': register_form
            }
        return render(request, 'account_module/register.html', context)

class LoginView(View):
    def get(self, request):
        login_form = LoginForm()
        context = {
            'login_form' : login_form
        }
        return render(request, 'account_module/login.html', context )

    def post(self, request):
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            user_email = login_form.cleaned_data.get('email')
            user_password = login_form.cleaned_data.get('password')
            user: User = User.objects.filter(email__iexact=user_email).first()
            if user is not None:
                if not user.is_active:
                    login_form.add_error('email','حساب کاربری فعال نمی باشد')
                else:
                    is_password_correct = user.check_password(user_password)
                    if is_password_correct:
                        login(request,user)
                        return redirect(reverse('home_page'))
                    else:
                        login_form.add_error('email','کاربر یافت نشد')
            else:
                login_form.add_error('email','کاربر یافت نشد')

        context = {
            'login_form': login_form
        }
        return render(request, 'account_module/login.html', context)

class ActivateAccountView(View):
    def get(self,request,email_active_code):
        user :User = User.objects.filter(email_active_code__iexact=email_active_code).first()
        if user is not None:
            if not user.is_active:
                user.is_active = True
                user.is_active_code = get_random_string(72)
                user.save()
                return redirect(reverse('login_page'))
        raise Http404

class ForgetPasswordView(View):
    def get(self,request):
        forget_pass_form = ForgotPassForm
        send_mail('فعالسازی حساب کاربری', new_user.email, {'user': new_user}, 'emails/active_account.html')
        context = {
            'forget_pass_form': ForgotPassForm
        }
        return render(request, 'account_module/forgot_pass.html', context)

class ResetPasswordView(View):
    def get(self,request,active_code):
        user :User = User.objects.filter(email_active_code__iexact=active_code)
        if user is None:
            return redirect(reverse('login_page'))
        reset_pass_form = ResetPassForm
        context = {
            'reset_pass_form' : reset_pass_form
        }
        return render(request,'account_module/reset_pass.html',context)
    def post(self,request,active_code):
        reset_pass_form = ResetPassForm(request.post)
        if reset_pass_form.is_valid():
            user : User= User.objects.filter(email_active_code__iexact=active_code).first()
            if user is None:
                return redirect(reverse('login_page'))
            user_new_pass = reset_pass_form.cleaned_data.get('password')
            user.email.active_code = get_random_string(72)
            user.is_active = True
            user.save()
            return redirect(reverse('login_page'))

class LogoutView(View):
    def get(self,request):
        logout(request)
        return redirect(reverse('login_page'))

