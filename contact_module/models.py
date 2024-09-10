from django.db import models


# Create your models here.

class ContactUs(models.Model):
    fullname = models.CharField(max_length=250, verbose_name='FullName')
    email = models.EmailField(max_length=300, verbose_name='Email Address')
    subject = models.CharField(max_length=250, verbose_name='Subject', blank=True, null=True)
    message = models.TextField(verbose_name='Message')
    created_time = models.DateTimeField(auto_now_add=True, verbose_name='Create Time')
    response = models.TextField(verbose_name='Admin Response', blank=True, null=True)
    is_read_by_admin = models.BooleanField(default=False, verbose_name='Reade By Admin')

    class Meta:
        verbose_name = 'پیام'
        verbose_name_plural = 'پیام ها'

    def __str__(self):
        return self.fullname


class UserProfile(models.Model):
    """
    when we set the upload_to attribute ,
    automatically file will be uploaded in MEDIA_ROOT address
    """
    # generally files
    # image = models.FileField(upload_to='images/%Y/%m')
    # specially images with pillow , the html form just accept the images
    image = models.ImageField(upload_to='images/%Y/%m')

    def __str__(self):
        return self.image
