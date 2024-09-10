import os
from django.views.generic import ListView
from recipes.models import Recipe
from utils.pagination import make_pagination
from django.db.models import Q


PER_PAGE = int(os.environ.get('PER_PAGE', 6))

class RecipeListViewBase(ListView):
    model = Recipe
    context_object_name = 'recipes'
    paginate_by = None
    ordering = ['-id']
    template_name = 'recipes/pages/home.html'

    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        qs = qs.filter(is_published=True)
        return qs
        

    def get_context_data(self, *args, **kwargs):
        ctx = super().get_context_data(*args, **kwargs)
        page_obj, pagination_range = make_pagination(self.request, ctx.get('recipes'), PER_PAGE)
        ctx.update({'recipes': page_obj, 'pagination_range': pagination_range})
        return ctx

    

class RecipeListViewHome(RecipeListViewBase):
    template_name = 'recipes/pages/home.html'


class RecipeListViewcategory(RecipeListViewBase):
    template_name = 'recipes/pages/category.html'

    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        qs = qs.filter(category__id=self.kwargs.get('category_id'))
        return qs
        



class RecipeListViewSearch(RecipeListViewBase):
    template_name = 'recipes/pages/search.html'

    def get_queryset(self, *args, **kwargs):
        search_term = self.request.GET.get('q', '')
        qs = super().get_queryset(*args, **kwargs)
        qs = qs.filter(Q(Q(title__icontains=search_term) | Q(description__icontains=search_term),), is_published=True).order_by('-id')
        return qs
    
    def get_context_data(self, *args, **kwargs):
        ctx = super().get_context_data(*args, **kwargs)
        search_term = self.request.GET.get('q', '')
        ctx.update({'page_title': f'Search for "{search_term}"', 'search_term': search_term, 'additional_url_query': f'&q={search_term}',})
        return ctx