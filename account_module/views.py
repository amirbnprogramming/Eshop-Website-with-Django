# Django Packages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from django.core.mail import EmailMultiAlternatives
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.crypto import get_random_string
from django.utils.html import strip_tags
from django.views import View

# apps Packages
from account_module.forms import RegisterForm, LoginForm, PasswordRecoveryForm, PasswordResetForm
from account_module.models import User, ActivationCode
from eshopProject import settings
from utils.email_service import send_email


# Create your views here.
class RegisterView(View):
    def get(self, request):
        register_form = RegisterForm()
        context = {
            'register_form': register_form
        }
        return render(request, 'account_module/register_page.html', context)

    def post(self, request):
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            # First we check if the email is added or not ?
            user_email = register_form.cleaned_data.get('email')
            user_password = register_form.cleaned_data.get('password')

            new_user: bool = User.objects.filter(email__iexact=user_email).exists()
            if new_user:
                register_form.add_error('email', 'ایمیل وارد شده قبلا در سیستم ثبت شده است')
            else:
                # get_random_string(72) give us a 72 character coded string
                user = User.objects.create(
                    email=user_email,
                    email_active_code=get_random_string(72),
                    is_active=False,
                    username=user_email,
                    password=make_password(user_password),
                )
                user.save()
                # todo: send email active code
                send_email(user)
                return redirect(reverse('login_page'))

            context = {
                'register_form': register_form
            }
            return render(request, 'account_module/register_page.html', context)

        context = {
            'register_form': register_form
        }
        return render(request, 'account_module/register_page.html', context)


class ActivateAccountView(View):
    def get(self, request, email_active_code):
        activation_record = ActivationCode.objects.get(code=email_active_code)
        user = User.objects.get(id=activation_record.user.id)
        if activation_record is not None and not user.is_active:
            try:
                user.is_active = True
                user.save()
                activation_record.delete()
                return redirect('login_page')
            except ActivationCode.DoesNotExist:
                return HttpResponse("Invalid activation code or the code has already been used.", status=400)
        else:
            return HttpResponse("Email was activated before.", status=400)


class LoginView(View):
    def get(self, request):
        login_form = LoginForm()
        context = {
            'login_form': LoginForm
        }
        return render(request, 'account_module/login_page.html', context)

    def post(self, request):
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            user_email = login_form.cleaned_data.get('email')  # extract email from posted form
            user_pass = login_form.cleaned_data.get('password')
            user: User = User.objects.filter(email__iexact=user_email).first()

            # First check availability of email
            # Then check account is_active
            # Then check correct password
            if user is None:
                login_form.add_error('email', 'کاربری با مشخصات وارد شده یافت نشد')
            else:
                if user.is_active:
                    # make input pass to hashable format and check
                    is_password_correct = user.check_password(user_pass)
                    if is_password_correct:
                        login(request, user)  # set the cookie and session id automatically
                        return redirect(reverse('user_panel_dashboard'))
                    else:
                        login_form.add_error('password', 'رمز عبور اشتباه است')
                else:
                    login_form.add_error('email', 'حساب کاربری شما فعال نیست')

        context = {
            'login_form': login_form
        }
        return render(request, 'account_module/login_page.html', context)


class PassWordRecoveryView(View):
    def get(self, request):
        password_recovery_form = PasswordRecoveryForm()
        context = {'password_recovery_form': password_recovery_form}
        return render(request, 'account_module/password_recovery_page.html', context)

    def post(self, request):
        """
        1- check the email exists in the database
        2- generate a password recovery link or send active code
        3- send it as email to user
        4- Show new password configuration form
        5- register the new password
        6- redirect to login page
        """
        password_recovery_form = PasswordRecoveryForm(request.POST)
        if password_recovery_form.is_valid():
            user_email = password_recovery_form.cleaned_data.get('email')
            user: User = User.objects.filter(email__iexact=user_email).first()
            if user is not None:
                # destination_email = user.email
                # email_content = ''
                # todo: Send email to user contains activated_code as a link
                return redirect(reverse('index_page'))

            else:
                password_recovery_form.add_error('email', 'ایمیل یافت نشد!')
                context = {'password_recovery_form': password_recovery_form}
                return render(request, 'account_module/password_recovery_page.html', context)


class PassWordResetView(View):
    def get(self, request, active_code):
        """
        1- find the user in database with a same email active code as the active_code in url
        2- if the url is not valid , redirect to login page
        3- if the url is valid , render the password_reset_page.html page to reset the password
        """
        user = User.objects.filter(email_active_code__iexact=active_code).first()  # Find the user
        if user is None:
            return redirect(reverse('login_page'))
        else:
            password_reset_form = PasswordResetForm()
            context = {
                'password_reset_form': password_reset_form,
                'user': user,
            }
            return render(request, 'account_module/password_reset_page.html', context)

    def post(self, request: HttpRequest, active_code):
        """
        1- send the request to make model form
        2- extract the new entered password from the form
        3- set_password to user model table (hash format password)
        4- generate new email active code
        5- save the user in database
        """
        password_reset_form = PasswordResetForm(request.POST)
        user = User.objects.filter(email_active_code__iexact=active_code).first()  # Find the user
        if password_reset_form.is_valid():
            if user is None:
                return redirect(reverse('login_page'))

            user_new_password = password_reset_form.cleaned_data['new_password']
            user.set_password(user_new_password)
            user.email_active_code = get_random_string(72)  # generate new active code for future
            user.is_active = True
            user.save()
            return redirect(reverse('login_page'))

        context = {
            'reset_pass_form': password_reset_form,
            'user': user,
        }

        return render(request, 'account_module/password_reset_page.html', context)


@login_required
def logout_view(request):
    logout(request)
    return redirect('login_page')


def send_email(user):
    activation_code, status = ActivationCode.objects.get_or_create(user=user)

    user_detail = {
        'subject': 'Activate Your Account',
        'name': user.first_name,
        'code': activation_code.code,
        'date_of_creation': user.date_joined,
    }

    html_content = render_to_string('account_module/email.html', context=user_detail)
    email_from = settings.DEFAULT_FROM_EMAIL
    recipient_list = [user.email]

    text_content = strip_tags(html_content)

    email = EmailMultiAlternatives(user_detail['subject'], text_content, email_from, recipient_list)
    email.attach_alternative(html_content, "text/html")

    email.send()
