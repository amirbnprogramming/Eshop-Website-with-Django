from django import forms
from django.core import validators

from account_module.models import User


# Customize connection between form and model , in fact with a Customized Form (Special Fields)
# Exactly the model fields
class UserEditProfileModelForm(forms.ModelForm):
    class Meta:
        # select the father model
        model = User
        # we specify which field will appear in form and take value from user
        fields = ['first_name', 'last_name', 'avatar', 'address', 'about_user']
        widgets = {
            'first_name': forms.TextInput(attrs={
                'placeholder': 'نام',
                'class': 'form-control',
            }),
            'last_name': forms.TextInput(attrs={
                'placeholder': 'نام خانوادگی',
                'class': 'form-control',
            }),
            'avatar': forms.FileInput(attrs={
                'class': 'form-control',
            }),
            'address': forms.Textarea(attrs={
                'placeholder': 'تهران خیابان آرزانتین ...',
                'class': 'form-control',
                'rows': 3,
                'id': 'message',
            }),
            'about_user': forms.Textarea(attrs={
                'placeholder': 'درباره ی کاربر',
                'class': 'form-control',
                'rows': 6,
                'id': 'message',
            })
        }
        labels = {
            'first_name': 'نام',
            'last_name': 'نام خانوادگی',
            'avatar': 'تصویر آواتار',
            'address': 'آدرس سکونت',
            'about_user': 'درباره کاربر',

        }


class UserEditPasswordForm(forms.Form):
    current_password = forms.CharField(
        label='رمزعبور قبلی',
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
            }
        ),
        validators=[
            validators.MaxLengthValidator(100),
        ]
    )
    new_password = forms.CharField(
        label='رمزعبور جدید',
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
            }),
        validators=[
            validators.MaxLengthValidator(100),
        ]
    )
    confirm_new_password = forms.CharField(
        label='تکرار رمز عبور جدید',
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
            }
        ),
        validators=[
            validators.MaxLengthValidator(100),
        ]
    )

    # Validators :

    def clean_confirm_password(self):
        password = self.cleaned_data.get('new_password')
        confirm_password = self.cleaned_data.get('confirm_new_password')

        if password == confirm_password:
            return confirm_password

        raise forms.ValidationError('کلمه عبور جدید و تکرار آن با یکدیگر مغایرت دارند')
