from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic.base import TemplateView, View
from django.views.generic import ListView,DetailView
from site_module.models import SiteBanner
from utils.http_service import get_client_ip
from utils.conventors import group_list

from .models import Product, ProductCategory, ProductBrand, ProductVisit, ProductGallery
from django.http import Http404
from django.db.models import Avg, Min, Max, Count


# class ProductTemplateView(TemplateView):
#     template_name = 'product_module/product_list.html'
#     def get_context_data(self, **kwargs):
#         products = Product.objects.all().order_by('price')[:5]
#         context= super(ProductTemplateView,self).get_context_data()
#         context['data'] = products
#         return context


# class ProductDetailTemplateView(TemplateView):
#     template_name = 'product_module/product_detail.html'
#     def get_context_data(self, **kwargs):
#         product= Product.objects.all()
#         context= super(ProductDetailTemplateView,self).get_context_data()
#         context['data'] = product
#         return context

class ProductDetailListView(DetailView):
    template_name = 'product_module/product_detail.html'
    model = Product


    def get_context_data(self, **kwargs):
        context= super(ProductDetailListView,self).get_context_data()
        context['banner']= SiteBanner.objects.filter(is_active=True,position=SiteBanner.SiteBannerPosition.product_detail)
        loaded_product= self.object
        request= self.request
        user_ip= get_client_ip(self.request)
        user_id= None
        if request.user.is_authenticated:
            user_id=request.user.id
        has_been_visited= ProductVisit.objects.filter(ip__iexact=user_ip,product_id=loaded_product.id).exists()
        if not has_been_visited:
            new_visit= ProductVisit(ip= user_ip,user_id=user_id,product_id=loaded_product.id)
            new_visit.save()
        product_gallery = group_list(list(ProductGallery.objects.filter(product_id=loaded_product.id).all()),3)
        context['product_gallery'] = product_gallery
        return context

class ProductListView(ListView):
    template_name = 'product_module/product_list.html'
    model = Product
    context_object_name = 'products'
    ordering = ['price']
    paginate_by = 6

    def get_context_data(self, *, object_list=None, **kwargs):
        context= super(ProductListView,self).get_context_data()
        query = Product.objects.all()
        product:Product = query.order_by('-price').first()
        db_max_price= product.price if product is not None else 0
        context['start_price']= self.request.GET.get('start_price') or 0
        context['end_price']= self.request.GET.get('end_price') or db_max_price
        context['db_max_price']= db_max_price
        context['banner']=SiteBanner.objects.filter(is_active=True, position=SiteBanner.SiteBannerPosition.product_list)
        return context


    def get_queryset(self):
        query= super(ProductListView,self).get_queryset()
        category_name= self.kwargs.get('cat')
        brand_name= self.kwargs.get('brand')
        request= self.request
        start_price= request.GET.get('start_price')
        end_price= request.GET.get('end_price')
        if start_price is not None:
            query= query.filter(price__gte=start_price)
        if end_price is not None:
            query= query.filter(price__lte=end_price)
        if brand_name is not None:
            query = query.filter(brand__url_title__iexact=brand_name)
        if category_name is not None:
            query= query.filter(category__url_title__iexact=category_name)
        return query


    # def get_queryset(self):
    #     query_set= super(ProductListView,self).get_queryset()
    #     data = query_set.filter(is_active = True)
    #     return data

# class ProductListView(ListView):
#     template_name = 'product_module/product_list.html'
#     model = Product
#     context_object_name = 'products'
#
#     def get_queryset(self):
#         base_query = super(ProductListView,self).get_queryset()
#         data = base_query.filter(is_active = True)
#         return data
#     def get_context_data(self, *, object_list=None, **kwargs):
#         context = super(ProductListView,self).get_context_data()
#         context['banner'] = SiteBanner.objects.filter(is_active=True,position__exact=SiteBanner.SiteBannerPosition.product_list)
#         return context
class AddFavoriteProduct(View):
    def post(self,request):
        product_id = request.POST['product_id']
        product = Product.objects.get(pk = product_id)
        request.session['product-favorite'] = product_id
        return redirect(product.get_absolute_url())


def product_cateegories_components(request):
    product_category= ProductCategory.objects.filter(is_active=True,is_delete=False)
    context= {
        'product_category': product_category
        }
    return render(request,'product_module/components/product_categories_components.html',context)


def product_brands_components(request):
    brands= ProductBrand.objects.annotate(products_count=Count('product')).filter(is_active=True)
    context= {
        'brands': brands
    }
    return render(request,'product_module/components/product_brands_components.html',context)