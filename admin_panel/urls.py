from django.urls import path

from admin_panel import views

urlpatterns = [
    path('', views.index, name='admin_dashboard_view'),
    path('articles/', views.ArticlesListView.as_view(), name='admin_article_view'),
    path('articles/<pk>/', views.ArticleEditView.as_view(), name='admin_article_edit_view'),
]