from django.db import models
from django.urls import reverse
from django.utils.text import slugify

from account_module.models import User


# Create your models here.
class ProductCategory(models.Model):
    title = models.CharField(max_length=360,db_index=True,verbose_name= 'عنوان')
    url_title= models.CharField(max_length=100,blank=True,null=True,verbose_name='عنوان در url')
    is_active = models.BooleanField(verbose_name= 'فعال/غیرفعال')
    is_delete = models.BooleanField(verbose_name='حذف شده/نشده')
    def __str__(self):
        return f"( {self.title} - {self.url_title})"
    class Meta:
        verbose_name = 'دسته بندی'
        verbose_name_plural = 'دسته بندی ها'

class ProductBrand(models.Model):
    title = models.CharField(max_length=300 ,db_index=True, verbose_name= 'نام برند')
    url_title = models.CharField(max_length=100, blank=True, null=True, verbose_name='عنوان در url')
    is_active = models.BooleanField(verbose_name= 'فعال/غیرفعال')

    def __str__(self):
        return f"{self.title}"
    class Meta:
        verbose_name = 'برند'
        verbose_name_plural = 'برند ها'

class ProductGallery(models.Model):
    product = models.ForeignKey('Product', on_delete=models.CASCADE, verbose_name= 'محصول' )
    image = models.ImageField(upload_to='product_gallery', verbose_name='تصویر گالری')

    def __str__(self):
        return self.product.title
    class Meta:
        verbose_name = 'تصویر گالری'
        verbose_name_plural = 'گالری تصاویر'


class Product(models.Model):
    title = models.CharField(max_length=300, verbose_name='نام محصول')
    category = models.ManyToManyField(ProductCategory, related_name='product_categories', verbose_name='دسته بندی')
    image = models.ImageField(upload_to= 'images/products',null=True, blank= True, verbose_name= 'تصویر محصول')
    brand = models.ForeignKey(ProductBrand, on_delete=models.CASCADE, verbose_name='برند', null=True, blank=True)
    price = models.IntegerField(verbose_name='قیمت')
    short_description = models.CharField(max_length=360, null=True, db_index=True, verbose_name='توضیحات کوتاه')
    description = models.TextField(verbose_name='توضیحات اصلی ', db_index=True)
    is_active = models.BooleanField(default=False, verbose_name='فعال/غیرفعال', max_length=300)
    slug = models.SlugField(default="", null=False, db_index=True, blank=True, unique=True, verbose_name='عنوان در url')
    is_delete = models.BooleanField(verbose_name='حذف شده/ نشده')

    def __str__(self):
        return f"{self.title} ( {self.price})"

    class Meta:
        verbose_name = 'محصول'
        verbose_name_plural = 'محصولات'

    def get_absolute_url(self):
        return reverse('product-detail', args=[self.slug])

    # def get_absolute_url(self):
    #     return reverse('product-detail', args=[self.slug])

    def save(self, *args, **kwargs):
        # self.slug = slugify(self.title)
        super().save(*args, **kwargs)

class ProductTag(models.Model):
    caption = models.CharField(max_length=300,db_index=True,verbose_name='عنوان')
    product = models.ForeignKey(Product, on_delete=models.CASCADE,verbose_name='product')

    def __str__(self):
        return f'{self.caption}'

    class Meta:
        verbose_name ='تگ محصول'
        verbose_name_plural = ' تگ های محصولات'

class ProductVisit(models.Model):
    product= models.ForeignKey(Product,on_delete=models.CASCADE,verbose_name='محصول')
    ip= models.CharField(max_length=100,verbose_name='آی پی')
    user= models.ForeignKey(User,blank=True,null=True,on_delete=models.CASCADE,verbose_name='کاربر')

    def __str__(self):
        return f'{self.product.title} / {self.ip}'

    class Meta:
        verbose_name= 'بازدید کاربر'
        verbose_name_plural= 'بازدیدهای کاربران'
