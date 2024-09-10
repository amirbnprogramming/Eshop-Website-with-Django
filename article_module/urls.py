from django.urls import path
from . import views

urlpatterns = [
    # path('', views.ArticleView.as_view(), name='articles'),
    path('', views.ArticleListView.as_view(), name='articles'),
    path('cat/<str:category>', views.ArticleListView.as_view(), name='articles_by_cat_list'),
    path('<int:pk>/', views.ArticleDetailView.as_view(), name='article_detail'),
    path('add-article-comment/', views.add_article_comment, name='add_article_comment'),

]
