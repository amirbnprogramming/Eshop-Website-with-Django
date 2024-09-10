from django import forms

from contact_module.models import ContactUs


# Customize connection between form and model , in fact with a Customized Form (Special Fields)
class ContactUsForm(forms.Form):
    fullname = forms.CharField(
        label='FullName',
        max_length=30,
        error_messages={
            'required': 'Enter Valid Name',
            'max_length': 'Full name must be at last 30 characters',
        },
        widget=forms.TextInput(attrs={
            'placeholder': 'First name & Last name',
            'class': 'form-control',
        }))

    email = forms.EmailField(
        label='Email',
        widget=forms.EmailInput(attrs={
            'placeholder': 'Email',
            'class': 'form-control',
        }))

    subject = forms.CharField(
        label='Subject',
        widget=forms.TextInput(attrs={
            'placeholder': 'Subject',
            'class': 'form-control',
        }))

    message = forms.CharField(
        label='Message',
        widget=forms.Textarea(
            attrs={
                'placeholder': 'Your Message',
                'class': 'form-control',
                'rows': 5,
                'id': 'message',
            }))


# Exactly the model fields
class ContactModelForm(forms.ModelForm):
    class Meta:
        # select the father model
        model = ContactUs
        # we specify which field will appear in form and take value from user
        fields = ['fullname', 'email', 'subject', 'message']
        widgets = {
            'fullname': forms.TextInput(attrs={
                'placeholder': 'First name & Last name',
                'class': 'form-control',
            }),
            'email': forms.TextInput(attrs={
                'placeholder': 'Enter your email',
                'class': 'form-control',
            }),
            'subject': forms.TextInput(attrs={
                'placeholder': 'Subject of message',
                'class': 'form-control',
            }),
            'message': forms.Textarea(attrs={
                'placeholder': 'Your Message',
                'class': 'form-control',
                'rows': 5,
                'id': 'message',
            })
        }
        labels = {
            'fullname': 'Fullname',
            'email': 'Email',
            'subject': 'Subject',
            'message': 'Message',
        }
        error_messages = {

            'fullname': {
                'required': 'Fullname field is compulsory',
                'max_length': 'Fullname must be at last 250 characters',
            },
            'email': {
                'required': 'Email field is compulsory'
            },
            'subject': {
                'required': 'Subject field is compulsory',
                'max_length': 'max_length must be at last 250 characters',
            },
            'message': {
                'required': 'Message field is compulsory'
            },
        }


class CreateProfileForm(forms.Form):
    user_image = forms.ImageField()
