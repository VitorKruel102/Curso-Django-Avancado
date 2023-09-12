from django.shortcuts import render, get_list_or_404, get_object_or_404, Http404
from django.db.models import Q # Pesquisa mais avançada no search
from django.contrib import messages
from django.views.generic import ListView

from utils.pagination import make_pagination
from recipes.models import Recipe

import os

PER_PAGE = int(os.environ.get('PER_PAGE', 6))

class RecipeListViewBase(ListView):
    model = Recipe
    context_object_name = 'recipes'
    ordering = ['-id']
    template_name = 'recipes/pages/home.html'

    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        qs = qs.filter(
            is_published=True,
        )
        return qs

    def get_context_data(self, *args, **kwargs):
        ctx = super().get_context_data(*args, **kwargs)
        page_obj, pagination_range = make_pagination(
            self.request,
            ctx.get('recipes'),
            PER_PAGE
        )
        ctx.update(
            {'recipes': page_obj, 'pagination_range': pagination_range}
        )
        return ctx




# Create your views here.
def home(request):
    recipes = Recipe.objects.filter( 
            is_published=True
    ).order_by('-id')

    page_obj, pagination_range = make_pagination(request, recipes, PER_PAGE)

    return render(
        request, 
        'recipes/pages/home.html', 
        context={
            'recipes': page_obj,
            'pagination_range': pagination_range
        }
    )

def category(request, category_id):
    recipes = get_list_or_404(
        Recipe.objects.filter(
            category__id=category_id, 
            is_published=True
        ).order_by('-id')
    )

    page_obj, pagination_range = make_pagination(request, recipes, PER_PAGE)

    return render(
        request, 
        'recipes/pages/category.html', 
        context={
            'recipes': page_obj,
            'pagination_range': pagination_range,
            'title_category': f'{recipes[0].category.name} - Category |',
        }
    )

def recipe(request, id):
    recipe = get_object_or_404(Recipe, pk=id, is_published=True)

    return render(
        request, 
        'recipes/pages/recipe-view.html', 
        context={
            'recipe': recipe,
            'is_detail_page': True,
        }
    )

def search(request):

    search_term = request.GET.get('search', '').strip()
    
    if not search_term:
        raise Http404()
        
    """
    contains = encontra a palavra exata;
    icontains = encontra a palavra sendo em minuscula ou maiscula;
    """
    recipes = Recipe.objects.filter(
        Q(
            Q(title__icontains=search_term) | 
            Q(description__icontains=search_term)
        ),
        is_published=True,
    ).order_by('-id')

    page_obj, pagination_range = make_pagination(request, recipes, PER_PAGE)

    return render(
        request, 
        'recipes/pages/search.html', 
        context={
            'page_title': f'Search for "{search_term}" | ',
            'search_term': search_term,
            'recipes': page_obj,
            'pagination_range': pagination_range,
            'additional_url_query': f'&search={search_term}',
        }
    )
