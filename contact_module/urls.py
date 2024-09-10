from django.urls import path
from . import views

urlpatterns = [
    # path('', views.contact_us_page, name='contact_us_page'),                               # function base view
    path('', views.ContactUsView.as_view(), name='contact_us_page'),                         # class base view
    path('create-profile/', views.CreateProfileView.as_view(), name='create_profile_page'),  # class base view
    path('profiles/', views.ProfileListView.as_view(), name='profiles_page'),                # class base view
]
