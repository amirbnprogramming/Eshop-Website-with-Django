from django.urls import path

from . import views

urlpatterns = [
    # path('', views.product_list, name='product_list'),
    # path('<slug:url_slug>/', views.product_detail, name='product-detail'),

    path('', views.ProductListView.as_view(), name='product_list'),
    path('cat/<cat>', views.ProductListView.as_view(), name='product_categories_list'),
    path('brands/<brand>', views.ProductListView.as_view(), name='product_brands_list'),

    path('product-favorite/', views.AddProductFavoriteView.as_view(), name='product-favorite'),
    path('<slug:slug>/', views.ProductDetailView.as_view(), name='product-detail'),

]
