from django.db.models import Count
from django.shortcuts import render
from django.views import View
from django.views.generic import TemplateView

from product_module.models import Product, ProductCategory, ProductGallery
from utils.conventors import group_list
from site_module.models import SiteSetting, FooterLinkBox, FooterLink, Slider
from django.db.models import Sum, F



class HomeView(TemplateView):
        template_name = 'home_module/index_page.html'
        def get_context_data(self, **kwargs):
            context= super().get_context_data(**kwargs)
            sliders = Slider.objects.filter(is_active=True)
            context['sliders'] = sliders
            lateast_products= Product.objects.filter(is_active=True,is_delete=False).order_by('-id')[:12]
            most_bought_product = Product.objects.filter(orderdetails__order__is_paid=True).\
                annotate(order_count =Sum('orderdetails__count')).order_by('-order_count')[:12]
            most_visit_product = Product.objects.filter(is_active=True , is_delete=False).\
                annotate(visit_count =Count('productvisit')).order_by('-visit_count')[:12]
            context['most_bought_product'] = group_list(most_bought_product)
            context['most_visit_product'] = group_list(most_visit_product)
            context['lateast_products']= group_list(lateast_products)
            categories = list(ProductCategory.objects.filter(is_active=True,is_delete=False)[:6])
            categories_products= []
            for category in categories:
                item = {
                    'title': category.title,
                    'id': category.id,
                    'products': list(category.product_categories.all())
                }
                categories_products.append(item)
            context['categories_products']= categories_products
            return context

def site_header_component(request):
    setting: SiteSetting = SiteSetting.objects.filter(is_main_setting=True).first()
    context = {
        'site_setting': setting
    }
    return render(request, 'shared/site_header_component.html',context)

def site_footer_component(request):
    setting: SiteSetting = SiteSetting.objects.filter(is_main_setting=True).first()
    footer_link_box = FooterLinkBox.objects.all()
    context = {
        'site_setting': setting ,
        'footer_link_box': footer_link_box,
    }
    return render(request, 'shared/site_footer_component.html',context)




class AboutView(TemplateView):
    template_name = 'home_module/about_page.html'

    def get_context_data(self, **kwargs):
        context= super(AboutView,self).get_context_data(**kwargs)
        site_setting = SiteSetting.objects.filter(is_main_setting=True).first()
        context['site_setting'] = site_setting
        return context




