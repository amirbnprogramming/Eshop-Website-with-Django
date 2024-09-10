from django.db import models
from jalali_date import date2jalali, datetime2jalali

from account_module.models import User


# Create your models here.

class ArticleCategory(models.Model):
    title = models.CharField(max_length=200, verbose_name='دسته بندی مقالات')
    url_title = models.CharField(max_length=200, verbose_name='عنوان آدرس', unique=True)
    is_active = models.BooleanField(default=True, verbose_name='فعال / غیرفعال')
    parent = models.ForeignKey('ArticleCategory', on_delete=models.CASCADE, verbose_name='دسته بندی والد', null=True, blank=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'دسته بندی مقالات'
        verbose_name_plural = 'دسته بندی های مقالات'


class Article(models.Model):
    title = models.CharField(max_length=300, verbose_name='عنوان مقاله')
    slug = models.SlugField(max_length=400, db_index=True, verbose_name='عنوان در url', allow_unicode=True)
    image = models.ImageField(upload_to='images/articles/%Y/%m/%d', verbose_name='تصویر مقاله', null=True, blank=True)
    short_description = models.TextField(verbose_name='توضیحات کوتاه', null=True, blank=True)
    description = models.TextField(verbose_name='توضیحات', null=True, blank=True)
    is_active = models.BooleanField(default=True, verbose_name='فعال / غیرفعال')
    category = models.ManyToManyField(ArticleCategory, verbose_name='دسته بندی ها', blank=True)
    author = models.ForeignKey(User, editable=False, max_length=250, verbose_name='نویسنده', on_delete=models.CASCADE,
                               null=True, blank=True)
    published_date = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ انتشار', editable=True)

    # use jalali with functional way
    def get_jalali_create_date(self):
        return date2jalali(self.published_date)

    def get_jalali_create_time(self):
        return self.published_date.strftime('%H:%M')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'مقاله'
        verbose_name_plural = 'مقالات'


class ArticleComment(models.Model):
    article = models.ForeignKey(Article, verbose_name='مقاله', on_delete=models.CASCADE)
    parent = models.ForeignKey('self', verbose_name='در جواب', on_delete=models.CASCADE, null=True, blank=True)
    author = models.ForeignKey(User, verbose_name='نویسنده نظر', on_delete=models.CASCADE)
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ثبت')
    comment_text = models.TextField(verbose_name='متن نظر', null=True, blank=True)

    def __str__(self):
        return self.comment_text

    class Meta:
        verbose_name = 'نظر'
        verbose_name_plural = 'نظرات'
