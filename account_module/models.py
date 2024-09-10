"""
Abstract user contain default field of user table which we can see:
    username = models.CharField(
        _("username"),max_length=150,unique=True,help_text=_(
            "Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only."),validators=[username_validator],
        error_messages={"unique": _("A user with that username already exists."),},
    )
    first_name = models.CharField(_("first name"), max_length=150, blank=True)
    last_name = models.CharField(_("last name"), max_length=150, blank=True)
    email = models.EmailField(_("email address"), blank=True)
    is_staff = models.BooleanField(_("staff status"),default=False,
    help_text=_("Designates whether the user can log into this admin site."),)
    is_active = models.BooleanField( _("active"),default=True,help_text=_(
            "Designates whether this user should be treated as active. "
            "Unselect this instead of deleting accounts."),)
    date_joined = models.DateTimeField(_("date joined"), default=timezone.now)
"""
import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.

class User(AbstractUser):
    email_active_code = models.CharField(max_length=100, verbose_name='Email Verification Code', null=True, blank=True)
    avatar = models.ImageField(upload_to='images/user_avatar', verbose_name='User Picture', null=True, blank=True)
    about_user = models.TextField(null=True, verbose_name='درباره کاربر', blank=True)
    address = models.TextField(verbose_name='آدرس', blank=True, null=True)

    class Meta:
        verbose_name = 'کاربر'
        verbose_name_plural = 'کاربران'

    def __str__(self):
        if self.first_name != '' and self.last_name != '':
            return self.get_full_name()
        else:
            return self.username


class ActivationCode(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    code = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
