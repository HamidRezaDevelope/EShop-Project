from django.http import HttpResponse
from django.shortcuts import render
from django.views import View
from django.views.generic import DetailView
from django.views.generic.list import ListView
from jalali_date import datetime2jalali, date2jalali
from article_module.models import Article, ArticleCategory, ArticleComment


# Create your views here.

# class ArticleView(View):
#     def get(self,request):
#         articles = Article.objects.filter(is_active=True)
#         context = {
#             'articles': articles
#         }
#         return render(request,'article_module/article_page.html',context)
#
class ArticleListView(ListView):
    template_name = 'article_module/article_page.html'
    model = Article
    paginate_by = 1

    def get_queryset(self):
        query = super(ArticleListView,self).get_queryset()
        query = query.filter(is_active= True)
        category_name= self.kwargs.get('category')
        if category_name is not None:
            query = query.filter(selected_category__url_title__iexact= category_name)
        return query



class ArticleDetailView(DetailView):
    model = Article
    template_name = 'article_module/article_detail_page.html'

    def get_queryset(self):
        query= super(ArticleDetailView,self).get_queryset()
        query= query.filter(is_active= True)
        return query

    def get_context_data(self, **kwargs):
        context= super(ArticleDetailView,self).get_context_data()
        article= kwargs.get('object')
        context['comments']= ArticleComment.objects.filter(article_id=article.id,parent= None).order_by('-create_date').prefetch_related('articlecomment_set')
        context['comment_count'] = ArticleComment.objects.filter(article_id=article.id).count()
        return context



def article_categories_component(request):
    article_main_category= ArticleCategory.objects.filter(is_active= True,parent_id= None)
    context = {
        'article_main_category' : article_main_category
    }
    return render(request,'article_module/components/article_category_components.html',context)


def add_article_comment(request):
    if request.user.is_authenticated:
        article_comment= request.GET.get('article_comment')
        article_id= request.GET.get('article_id')
        parent_id = request.GET.get('parent_id')
        new_comment= ArticleComment(text= article_comment,parent_id=parent_id,article_id= article_id,user_id=request.user.id)
        new_comment.save()
        context= {
            'comments' : ArticleComment.objects.filter(article_id=article_id,parent= None).order_by('-create_date').prefetch_related('articlecomment_set'),
            'comment_count': ArticleComment.objects.filter(article_id=article_id).count()
        }
        return render(request,'article_module/include/article_comment_components.html',context)

    return HttpResponse('hello djangoo')
