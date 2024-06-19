
from django import forms
from contact_module.models import ContactUs

class ContactUsForm(forms.Form):
    full_name = forms.CharField(label='نام و نام خانوادگی',
    max_length=50,
    error_messages={
        'required' :'لطفا نام و نام خانوادگی خود را وارد کنید',
        'max_length' : 'نام نمیتواند بیشتر از 50 کاراکتر باشد'
    },
    widget=forms.TextInput(attrs={
        'class' : 'form-control',
        'placeholder' : 'نام و نام خانوادگی'
    }))
    email = forms.EmailField(label='ایمیل' ,widget= forms.EmailInput(attrs={
        'class': 'form-control',
        'placeholder': 'ایمیل'
    }

    ))
    title = forms.CharField(label='عنوان',widget=forms.TextInput(attrs={
        'class' : 'form-control',
        'placeholder' : 'عنوان'
    }))
    massage = forms.CharField(label='متن پیام',widget= forms.Textarea(attrs={
        'class':'form-control',
        'placeholder':'متن پیام',
        'id': 'massage'
    }))


class ContactUsModelForm(forms.ModelForm):
    class Meta:
        model = ContactUs
        fields = ['full_name', 'title', 'massage', 'email']
        widgets = {
            'full_name': forms.TextInput(attrs={
                'class': 'form-control'
            }),
            'email': forms.TextInput(attrs={
                'class': 'form-control'
            }),
            'title': forms.TextInput(attrs={
                'class': 'form-control'
            }),
            'massage': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 5,
                'id': 'massage'
            })
        }
        # fields = '__all__///'
        # exclude = ['full_name']

class ProfileForm(forms.Form):
    user_image = forms.ImageField()

