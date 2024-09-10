from django.urls import path

from account_module import views

urlpatterns = [
    path('register', views.RegisterView.as_view(), name='register_page'),
    path('login', views.LoginView.as_view(), name='login_page'),
    path('logout', views.logout_view, name='logout_page'),
    path('activate-code/<email_active_code>', views.ActivateAccountView.as_view(), name='activate_account'),
    path('password-recovery', views.PassWordRecoveryView.as_view(), name='password_recovery'),
    path('password-reset/<active_code>', views.PassWordResetView.as_view(), name='password_reset'),

]
