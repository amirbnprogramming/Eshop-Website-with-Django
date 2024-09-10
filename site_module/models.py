from django.db import models


# Create your models here.

class SiteSetting(models.Model):
    site_name = models.CharField(max_length=200, verbose_name='نام سایت')
    site_url = models.CharField(max_length=200, verbose_name='دامنه سایت')
    address = models.CharField(max_length=200, null=True, blank=True, verbose_name='آدرس شرکت')
    phone = models.CharField(max_length=200, null=True, blank=True, verbose_name='تلفن سایت')
    email = models.CharField(max_length=200, null=True, blank=True, verbose_name='ایمیل سایت')
    fax = models.CharField(max_length=200, null=True, blank=True, verbose_name='فکس شرکت')
    copy_write = models.TextField(verbose_name='متن کپی رایت سایت', null=True, blank=True)
    site_logo = models.ImageField(verbose_name='لوگو سایت', upload_to='images/site-setting/logo', null=True, blank=True)
    about_us_text = models.TextField(verbose_name='متن درباره ما', null=True, blank=True)
    is_main_setting = models.BooleanField(default=False, verbose_name='تنظیمات اصلی')

    class Meta:
        verbose_name = 'تنظیمات سایت'
        verbose_name_plural = 'تنظیمات'

    def __str__(self):
        return self.site_name


# title and subtitle in footer of the site
class FooterLinkBox(models.Model):
    title = models.CharField(max_length=200, verbose_name='عنوان')

    class Meta:
        verbose_name = 'دسته بندی لینک های فوتر'
        verbose_name_plural = 'دسته بندی های لینک های فوتر'

    def __str__(self):
        return self.title


class FooterLink(models.Model):
    title = models.CharField(max_length=200, verbose_name='عنوان')
    url = models.URLField(max_length=500, verbose_name='لینک')
    footer_link_box = models.ForeignKey(to=FooterLinkBox, verbose_name='دسته بندی', on_delete=models.CASCADE)

    class Meta:
        verbose_name = ' لینک فوتر'
        verbose_name_plural = 'لینک های فوتر'

    def __str__(self):
        return self.title


class Slider(models.Model):
    title = models.CharField(max_length=200, verbose_name='عنوان')
    description = models.TextField(verbose_name='توضیحات اسلایدر')
    url = models.URLField(max_length=500, verbose_name='آدرس')
    url_title = models.CharField(max_length=200, verbose_name='عنوان آدرس')
    image = models.ImageField(upload_to='images/slider_img', verbose_name='تصویر اسلایدر')
    is_active = models.BooleanField(default=True, verbose_name='فعال/غیرفعال')

    class Meta:
        verbose_name = 'اسلایدر'
        verbose_name_plural = 'اسلایدرها'

    def __str__(self):
        return self.title


# site_banner_positions = [
#     ('product_list', 'صفحه لیست محصولات'),
#     ('product_detail', 'صفحه جزئیات محصولات'),
# ]


class SiteBanner(models.Model):
    class SiteBannerPosition(models.TextChoices):
        product_list = 'product_list', 'صفحه لیست محصولات'
        product_detail = 'product_detail', 'صفحه جزئیات محصولات'
        about_us = 'about_us', 'صفحه درباره ما'

    title = models.CharField(max_length=200, verbose_name='عنوان بنر')
    url = models.URLField(max_length=400, verbose_name='آدرس بنر', null=True, blank=True)
    image = models.ImageField(verbose_name='تصویر بنر', upload_to='images/site_banner')
    is_active = models.BooleanField(verbose_name='فعال/غیرفعال')
    position = models.CharField(max_length=200, choices=SiteBannerPosition.choices, verbose_name='محل قرار گیری')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'بنر'
        verbose_name_plural = 'بنر ها'
