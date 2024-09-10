from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from django.views.generic import TemplateView
from django.views.generic.edit import FormView, CreateView
from django.views.generic import ListView

from site_module.models import SiteSetting
from .forms import ContactUsForm, ContactModelForm, CreateProfileForm
from .models import ContactUs, UserProfile

"""Contact Us"""


class ContactUsView(CreateView):
    template_name = 'contact_module/contact_us_page.html'
    form_class = ContactModelForm
    success_url = '/'
    """ automatically valid def will call. and save operation will apply"""

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        setting: SiteSetting = SiteSetting.objects.filter(is_main_setting=True).first()
        context['site_setting'] = setting

        return context


"""Profile List """


class ProfileListView(ListView):
    model = UserProfile
    template_name = 'contact_module/profiles_list_page.html'
    context_object_name = 'profiles'


"""Create Profile """


class CreateProfileView(CreateView):
    template_name = 'contact_module/create_profile_page.html'
    model = UserProfile
    fields = '__all__'
    success_url = '/contact-us/create-profile'

    # def save_file(file):
    #     with open('temp/images/image.jpg', 'wb+') as destination:
    #         for chunk in file.chunks():  # to use memory less : chunk chunk will be saved
    #             destination.write(chunk)

    # class CreateProfileView(View):
    #     def get(self, request):
    #         form = CreateProfileForm()
    #         return render(request, 'contact_module/create_profile_page.html', {
    #             'form': form
    #         })
    #
    #     def post(self, request):
    #         submitted_form = CreateProfileForm(request.POST, request.FILES)
    #
    #         if submitted_form.is_valid():
    #             # print(request.FILES['user-image'])
    #             # print(request.POST)
    #             # save_file(request.FILES['user-image'])     # directly save the file in folder
    #             # save file in database , but not exactly file , the address of it
    #             print(request.FILES)
    #             profile = UserProfile(image=request.FILES['user_image'])
    #             profile.save()
    #             return redirect('/contact-us/create-profile')
    #
    #         else:
    #             return render(request, 'contact_module/create_profile_page.html', {
    #                 'form': submitted_form
    #             })

    # class ContactUsView(FormView):
#     template_name = 'contact_module/contact_us_page.html'
#     form_class = ContactModelForm
#     """ return with the 'form' reserved name to the desired html page
#      return render(request, 'contact_module/contact_us_page.html', {
#          'form': contact_form
#      })
#      but how about the redirected page (sign of post successfully) ?
#      how about the resualt? are the posted data saved? we have  contact_form.save() command before
#      to do it we should specify the resault by valid or invalid form
#     """
#     success_url = '/contact-us/'
#
#     def form_valid(self, form):
#         form.save()
#         return super(ContactUsView, self).form_valid(form)

# class ContactUsView(View):
#     def get(self, request):
#         contact_form = ContactModelForm()
#         return render(request, 'contact_module/contact_us_page.html', {
#             'contact_form': contact_form
#         })
#
#     def post(self, request):
#         contact_form = ContactModelForm(request.POST)
#         if contact_form.is_valid():
#             contact_form.save()
#             return redirect('index_page')
#         else:
#             return render(request, 'contact_module/contact_us_page.html', {
#                 'contact_form': contact_form
#             })


# with Model forms
# def contact_us_page(request):
#     if request.method == 'POST':
#         request_content = request.POST
#         contact_form = ContactModelForm(request_content)  # automatically make the ContactUsForm fields full by data
#         if contact_form.is_valid():  # check each item validation : Email validation for email , Text validation for # name....
#             contact_form.save()  # automatically make a model instance and fill the fields in model in database
#             return redirect(reverse('index_page'))
#     else:
#         contact_form = ContactModelForm()  # make an object which has none value
#     return render(request, 'contact_module/contact_us_page.html', context={
#         'contact_form': contact_form
#     })

# With forms
# def contact_us_page(request):
#
#     if request.method == 'POST':
#         request_content = request.POST
#         contact_form = ContactUsForm(request_content)
#         # check each item validation : Email validation for email , Text validation for # name....
#         if contact_form.is_valid():
#             # make all the data in form clean (Html code >>to>> python dictionary )
#             filled_form = contact_form.cleaned_data
#             # fill the database model by the fields of form
#             contact_model = ContactUs(fullname=filled_form['fullname'],
#                                       email=filled_form['email'],
#                                       subject=filled_form['subject'],
#                                       message=filled_form['message'],
#                                       )
#             contact_model.save()
#             return redirect(reverse('index_page'))
#     else:
#         contact_form = ContactUsForm()  # make a object which has none value
#
#     return render(request, 'contact_module/contact_us_page.html', context={
#         'contact_form': contact_form
#     })

# Without Forms
# def contact_us_page(request):
# my_dict = {}
# if request.method == 'POST':
#     entered_email = request.POST['email']
#     if entered_email == '':
#         return render(request, 'contact_module/contact_us_page.html', context={
#             'has_error': True
#         })
#     for items in request.POST:
#         my_dict[items] = request.POST[items]
#
#     return redirect(reverse('index_page'))
