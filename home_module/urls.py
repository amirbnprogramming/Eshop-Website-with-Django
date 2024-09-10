from django.urls import path

from . import views

urlpatterns = [
    # path('', views.index_page, name='index_page'),
    path('', views.HomeView.as_view(), name='index_page'),
    path('about-us', views.AboutUsView.as_view(), name='about_us_page'),

]
