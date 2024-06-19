from django.db import models

# Create your models here.

class SiteSetting(models.Model):
    site_name = models.CharField(max_length=100 , verbose_name= 'نام سایت')
    site_url = models.CharField(max_length=100 , verbose_name=' دامنه سایت')
    about_us_text = models.TextField(max_length=100 , verbose_name= 'متن درباره ما')
    is_main_setting = models.BooleanField(max_length=100 , verbose_name= 'تنظیمات اصلی')
    email = models.CharField(max_length=100 ,null=True,blank=True, verbose_name= 'ایمیل')
    fax = models.CharField(max_length=100 ,null=True,blank=True, verbose_name= 'فکس')
    phone = models.CharField(max_length=100 ,null=True,blank=True, verbose_name= 'تلفن')
    address = models.CharField(max_length=100 , verbose_name= 'آدرس')
    copy_right = models.TextField(max_length=100 , verbose_name= 'متن کپی رایت')
    site_logo = models.ImageField(upload_to='images/site_setting', verbose_name=  'لوگو سایت')

    class Meta:
        verbose_name = 'تنظیمات سایت'
        verbose_name_plural = 'تنظیمات سایت'

    def __str__(self):
        return self.site_name



class FooterLinkBox(models.Model):
    title = models.CharField(max_length=100,verbose_name= 'عنوان')

    class Meta:
        verbose_name = 'دسته بندی لینکهای فوتر'
        verbose_name_plural = 'دسته بندی های لینکهای فوتر'

    def __str__(self):
        return self.title

class FooterLink(models.Model):
    title = models.CharField(max_length= 50,verbose_name= 'عنوان')
    url = models.URLField(max_length=500,verbose_name='لینک')
    footer_link_box = models.ForeignKey(to = FooterLinkBox,on_delete=models.CASCADE,verbose_name='دسته بندی')

    class Meta:
        verbose_name = 'لینک فوتر'
        verbose_name_plural = 'لینکهای فوتر'

    def __str__(self):
        return self.title

class Slider(models.Model):
    title = models.CharField(max_length=100,verbose_name='عنوان')
    url = models.URLField(max_length=200,verbose_name= 'لینک ')
    url_title = models.CharField(max_length=200,verbose_name= 'عنوان لینک')
    description = models.CharField(max_length=200,verbose_name= 'توضیحات اسلایدر ')
    image = models.ImageField(upload_to='images/sliders',verbose_name='تصویر اسلایدر')
    is_active = models.BooleanField(default=True,verbose_name='فعال/غیرفعال')

    class Meta:
        verbose_name = 'اسلایدر'
        verbose_name_plural = 'اسلایدرها'
    def __str__(self):
        return self.title

class SiteBanner(models.Model):
        class SiteBannerPosition(models.TextChoices):
            product_list = 'product_list','صفحه لیست محصولات',
            product_detail = 'product_detail','صفحه جزییات محصولات',
            about_us = 'about_us','صفحه درباره ما محصولات',

        title = models.CharField(max_length=200,verbose_name='عنوان')
        url = models.URLField(max_length=200,verbose_name='بنر')
        image = models.ImageField(upload_to='images/banners',verbose_name='تصویر بنر')
        is_active = models.BooleanField(max_length=200,verbose_name='فعال/غیرفعال')
        position = models.CharField(max_length=200,choices=SiteBannerPosition.choices,verbose_name='جایگاه نمایش')

        def __str__(self):
            return self.title

        class Meta:
            verbose_name = 'بنر تبلیغاتی'
            verbose_name_plural = 'بنر های تبلیغاتی'