from django.urls import path,re_path
from .import views

urlpatterns = [
    # path('',views.product_list,name = 'product-list'),
    path('',views.ProductListView.as_view(),name = 'product-list'),
    path('cat/<cat>',views.ProductListView.as_view(),name = 'product-categories-list'),
    path('brand/<brand>',views.ProductListView.as_view(),name = 'product-list-by-brand'),
    # path('product_detail',views.product_detail,name = 'product-detail'),
    path('product_favorite',views.AddFavoriteProduct.as_view,name = 'product-favorite'),
    path('<int:pk>',views.ProductDetailListView.as_view(),name = 'product-detail'),
]