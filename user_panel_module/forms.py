from django import forms
from django.core import validators

from account_module.models import User

# class ContactUsForm(forms.Form):
#     full_name = forms.CharField(label='نام و نام خانوادگی',
#     max_length=50,
#     error_messages={
#         'required' :'لطفا نام و نام خانوادگی خود را وارد کنید',
#         'max_length' : 'تام نمیتواند بیشتر از 50 کاراکتر باشد'
#     },
#     widget=forms.TextInput(attrs={
#         'class' : 'form-control',
#         'placeholder' : 'نام و نام خانوادگی'
#     }))
#     email = forms.EmailField(label='ایمیل' ,widget= forms.EmailInput(attrs={
#         'class': 'form-control',
#         'placeholder': 'ایمیل'
#     }
#
#     ))
#     title = forms.CharField(label='عنوان',widget=forms.TextInput(attrs={
#         'class' : 'form-control',
#         'placeholder' : 'عنوان'
#     }))
#     massage = forms.CharField(label='متن پیام',widget= forms.Textarea(attrs={
#         'class':'form-control',
#         'placeholder':'متن پیام',
#         'id': 'massage'
#     }))


class EditProfileModelForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'avatar', 'address','about_user']
        widgets = {
            'first_name': forms.TextInput(attrs={
                'class': 'form-control'
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'form-control'
            }),
            'avatar': forms.FileInput(attrs={
                'class': 'form-control'
            }),
            'address': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 1,
            }),
            'about_user':forms.Textarea(attrs={
                'class' : 'form-control',
                'rows' : 6,
                'id': 'massage'
            })

        }
        labels = {
            'first_name' :'نام',
            'last_name' :'نام خوانوادگی',
            'avatar' :'تصویر پروفایل',
            'address' :'آدرس',
            'about_user' : 'درباره شخص'
        }


        # fields = '__all__///'
        # exclude = ['full_name']


class ChangePasswordForm(forms.Form):
    current_password = forms.CharField(
        label='کلمه عبور فعلی',
        widget=forms.PasswordInput(
            attrs={
            'class' : 'form-control'
        }),
        validators=[
            validators.MaxLengthValidator(100),
        ]
    )
    password = forms.CharField(
        label='رمز عبور',
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control'
            }),
        validators=[
            validators.MaxLengthValidator(100),
        ]
    )
    confirm_password = forms.CharField(
        label='تکرار رمز عبور',
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control'
            },
        ),
        validators=[
            validators.MaxLengthValidator(100),
        ]
    )

    def clean_confirm_password(self):
        password = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data.get('confirm_password')
        if password == confirm_password:
            return confirm_password
