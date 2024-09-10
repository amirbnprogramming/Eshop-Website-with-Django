from django.urls import path

from user_panel_module import views

urlpatterns = [
    path('', views.UserPanelDashboardPage.as_view(), name='user_panel_dashboard'),
    path('user-edit-profile', views.UserEditProfilePage.as_view(), name='user_edit_profile'),
    path('user-edit-password', views.UserEditPasswordPage.as_view(), name='user_edit_password'),
    path('user-cart', views.user_cart, name='user_cart'),
    path('user-past-cart', views.UserPastCartsPage.as_view(), name='user_past_cart'),
    path('user-past-cart-detail/<order_id>', views.user_paid_factor_detail, name='user_past_cart_detail'),

    path('remove-order-detail', views.remove_order_detail, name='remove_order_detail_ajax'),
    path('change-order-detail', views.change_order_detail_count, name='change_order_detail_ajax'),

]