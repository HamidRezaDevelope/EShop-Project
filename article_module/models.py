from django.db import models

from account_module.models import User
from account_module.views import user


# Create your models here.

class ArticleCategory(models.Model):
    parent = models.ForeignKey('ArticleCategory',null=True,blank=True,on_delete=models.CASCADE,verbose_name='دسته بندی والد')
    title = models.CharField(max_length=300,verbose_name='عنوان')
    url_title = models.CharField(max_length=300,unique= True,verbose_name='عنوان در لینک')
    is_active = models.BooleanField(verbose_name='فعال/غیرفعال')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'دسته بندی مقاله'
        verbose_name_plural = 'دسته بندی های مقاله'


class Article(models.Model):
    title= models.CharField(max_length=300,verbose_name='عنوان مقاله')
    slug= models.SlugField(max_length=300,db_index=True,allow_unicode=True,verbose_name='عنوان در url')
    image= models.ImageField(upload_to='images/articles',verbose_name='تصویر مقاله')
    short_description= models.CharField(max_length=300,verbose_name='توضیحات کوتاه')
    is_active= models.BooleanField(verbose_name='فعال/غیرفعال')
    text = models.TextField(verbose_name='متن مقاله')
    selected_category = models.ManyToManyField('ArticleCategory',verbose_name='دسته بندی ها')
    author= models.ForeignKey(User,on_delete=models.CASCADE,null=True,verbose_name='نویسنده ها')
    create_date = models.DateTimeField(auto_now_add=True,editable=False,verbose_name='تاریخ ثبت')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name= 'مقاله'
        verbose_name_plural= 'مقالات'

class ArticleComment(models.Model):
    article=models.ForeignKey(Article,on_delete= models.CASCADE,verbose_name='مقاله')
    parent = models.ForeignKey('ArticleComment',on_delete=models.CASCADE,null=True,blank=True,verbose_name='والد')
    user= models.ForeignKey(User,on_delete=models.CASCADE,verbose_name='کاربر')
    create_date= models.DateTimeField(auto_now_add=True,verbose_name='تاریخ ثبت')
    text= models.TextField(verbose_name='متن نظر')

    def __str__(self):
        return str(self.user)

    class Meta:
        verbose_name= 'نظر مقاله'
        verbose_name_plural= 'نظرات مقاله'
