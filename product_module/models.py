from django.db import models
from django.urls import reverse
from django.utils.text import slugify

from account_module.models import User


class Brand(models.Model):
    name = models.CharField(max_length=300, db_index=True, verbose_name='Brand Name')
    url_name = models.CharField(max_length=300, db_index=True, verbose_name='Name in URLs')
    is_active = models.BooleanField(default=False, verbose_name='Activated/Deactivated')
    is_deleted = models.BooleanField(default=False, verbose_name='Deleted/Survive')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'برند'
        verbose_name_plural = 'برندها'


# Create your models here.
class Category(models.Model):
    title = models.CharField(max_length=300, db_index=True, verbose_name='Title')
    url_title = models.CharField(max_length=300, db_index=True, verbose_name='Title in url')
    is_active = models.BooleanField(default=False, verbose_name='Activated/Deactivated')
    is_deleted = models.BooleanField(default=False, verbose_name='Deleted/Survive')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'دسته بندی'
        verbose_name_plural = 'دسته بندی ها'


class Product(models.Model):
    brand = models.ForeignKey(Brand, db_index=True, verbose_name='Brand Name', on_delete=models.CASCADE)
    title = models.CharField(max_length=300, verbose_name='ProductName')
    category = models.ManyToManyField(Category, related_name='product_categories', verbose_name='Categories')
    price = models.IntegerField(verbose_name='Price')
    image = models.ImageField(upload_to='images/products', verbose_name='Product Image', blank=True, null=True)
    short_description = models.CharField(max_length=360, db_index=True, null=True, verbose_name='Short Description')
    description = models.TextField(verbose_name='Main Description', db_index=True)
    slug = models.SlugField(default="", null=False, db_index=True, blank=True, max_length=250, unique=True,
                            verbose_name='URL Title')  # sumsung galaxy s20 => sumsung-galaxy-s20
    is_active = models.BooleanField(default=False, verbose_name='Activated/Deactivated')
    is_deleted = models.BooleanField(default=False, verbose_name='Deleted/Survive')

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)  # sumsung galaxy s20 => sumsung-galaxy-s20
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('product-detail', args=[self.slug])

    class Meta:
        verbose_name = 'محصول'
        verbose_name_plural = 'محصولات'


class ProductTags(models.Model):
    caption = models.CharField(max_length=300, db_index=True, verbose_name='Title')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_tags')  # each tag for one

    # product

    def __str__(self):
        return self.caption

    class Meta:
        verbose_name = 'برچسب محصول'
        verbose_name_plural = 'برچسب های محصولات'


class ProductVisit(models.Model):
    product = models.ForeignKey('Product', on_delete=models.CASCADE, verbose_name='محصول')
    ip = models.CharField(max_length=30, verbose_name='آی پی کاربر')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='کاربری که مشاهده کرده', null=True,
                             blank=True)

    def __str__(self):
        return f'{self.product.title} / {self.ip}'

    class Meta:
        verbose_name = 'بازدید محصول'
        verbose_name_plural = 'بازدید های محصول'


class ProductGallery(models.Model):
    product = models.ForeignKey('Product', on_delete=models.CASCADE, verbose_name='محصول')
    image = models.ImageField(upload_to='images/product-gallery',verbose_name='تصویر')
    is_active = models.BooleanField(default=True, verbose_name='فعال/غیرفعال')

    def __str__(self):
        return self.product.title

    class Meta:
        verbose_name = 'تصویر گالری'
        verbose_name_plural = 'گالری تصاویر'
