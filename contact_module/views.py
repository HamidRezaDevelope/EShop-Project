from django.shortcuts import render,redirect
from django.urls import reverse
from django.views import View
from django.views.generic import ListView
from django.views.generic.edit import FormView,CreateView

from contact_module.forms import ContactUsForm, ContactUsModelForm, ProfileForm
from contact_module.models import ContactUs, UserProfile
from site_module.models import SiteSetting

class ContactUsFormView(FormView):
    template_name = 'contact_module/contact_us_page.html'
    form_class = ContactUsModelForm
    success_url = '/contact-us/'

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        contex= super().get_context_data(**kwargs)
        setting: SiteSetting= SiteSetting.objects.filter(is_main_setting= True).first()
        contex['setting']= setting
        return contex

# class ContactusView(View):
#     def get(self,request):
#         contact = ContactUsModelForm()
#         return render(request,'contact_module/contact_us_page.html',context={
#             'contact' : contact
#         })
#     def post(self,request):
#         contact = ContactUsModelForm(request.POST)
#         if contact.is_valid():
#             contact.save()
#             return redirect('home_page')
#
#         return render(request,'contact_module/contact_us_page.html',context={'contact':contact})

# class ContactUsView(CreateView):
#     form_class = ContactUsModelForm
#     template_name = 'contact_module/contact_us_page.html'
#     success_url = '/contact-us/'
#
#     def get_context_data(self, *args,**kwargs):
#         context = super().get_context_data(*args,**kwargs)
#         setting :SiteSetting = SiteSetting.objects.filter(is_main_setting= True).first()
#         context['site_setting'] = setting
#         return context

class CreateProfileView(CreateView):
    template_name = 'contact_module/create_profile_page.html'
    model = UserProfile
    fields = '__all__'
    success_url = '/contact-us/create-profile'
    # def get(self,request):
    #     form = ProfileForm()
    #     return render(request,'contact_module/create_profile_page.html',{
    #         'form' : form
    #     })
    # def post(self,request):
    #     submitted_form = ProfileForm(request.POST, request.FILES)
    #     if submitted_form.is_valid():
    #         profile = UserProfile(image= request.FILES['user_image'])
    #         profile.save()
    #     return render(request, 'contact_module/create_profile_page.html', {
    #         'form': submitted_form })


class ProfileList(ListView):
    template_name = 'contact_module/profile_list_page.html'
    model = UserProfile
    context_object_name = 'profiles'




