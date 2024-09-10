from django.http import HttpResponse
from django.shortcuts import render
from django.views import View
from django.views.generic import ListView, DetailView

from article_module.models import Article, ArticleCategory, ArticleComment


# Create your views here.

class ArticleView(View):
    def get(self, request):
        active_articles = Article.objects.filter(is_active=True).all()
        return render(request, 'article_module/articles_page.html', context={
            'active_articles': active_articles
        })


class ArticleListView(ListView):
    model = Article
    paginate_by = 1
    template_name = 'article_module/articles_page.html'
    context_object_name = 'active_articles'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        return context

    def get_queryset(self):
        query = super(ArticleListView, self).get_queryset()
        query = query.filter(is_active=True)
        category_name = self.kwargs.get('category')
        if category_name is not None:
            query = query.filter(category__url_title__iexact=category_name)
        return query


# categorization posts section :
def article_categories_component(request):
    active_main_article_categories = ArticleCategory.objects.filter(is_active=True, parent_id=None).prefetch_related('articlecategory_set')
    context = {
        'categories': active_main_article_categories
    }
    return render(request, 'article_module/includes/article_categories_component.html', context)


class ArticleDetailView(DetailView):
    model = Article
    template_name = 'article_module/article_detail_page.html'

    def get_queryset(self):
        query = super(ArticleDetailView, self).get_queryset()
        query = query.filter(is_active=True)
        return query

    def get_context_data(self, *args, **kwargs):
        context = super(ArticleDetailView, self).get_context_data()
        context_object_name = 'selected_article'
        article: Article = kwargs.get('object')
        # with prefetch , with one query we extract all the subcomments of the comment
        context['comments'] = ArticleComment.objects.filter(article_id=article.id, parent_id=None).order_by(
            '-create_time').prefetch_related(
            'articlecomment_set')
        context['comments_count'] = ArticleComment.objects.filter(article_id=article.id).count()
        return context


def add_article_comment(request):
    if request.user.is_authenticated:
        article_id = request.GET.get('article_id')
        article_comment = request.GET.get('article_comment')
        comment_author = request.user.id
        parent_id = request.GET.get('parent_id')
        new_comment = ArticleComment(article_id=article_id, comment_text=article_comment, author_id=comment_author,
                                     parent_id=parent_id)
        new_comment.save()

        context = {
            'comments': ArticleComment.objects.filter(article_id=article_id, parent_id=None).order_by(
                '-create_time').prefetch_related(
                'articlecomment_set'),
            'comments_count': ArticleComment.objects.filter(article_id=article_id).count()
        }

        return render(request, 'article_module/partial/article_comment_partial.html', context)

    return HttpResponse('Sent')

