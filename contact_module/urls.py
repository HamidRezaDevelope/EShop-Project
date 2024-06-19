from django.urls import path
from . import views

urlpatterns = [
    path('',views.ContactUsFormView.as_view(),name= 'contact_us_page'),
    path('create-profile',views.CreateProfileView.as_view(),name= 'create_profile_page'),
    path('profile_list',views.ProfileList.as_view(),name = 'profile_list_page')
]