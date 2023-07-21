from django.shortcuts import render, get_list_or_404, get_object_or_404, Http404
from django.db.models import Q # Pesquisa mais avançada no search
from utils.recipes.factory import make_recipe

from recipes.models import Recipe

# Create your views here.
def home(request):
    recipes = Recipe.objects.filter( 
            is_published=True
    ).order_by('-id')
    
    return render(
        request, 
        'recipes/pages/home.html', 
        context={
            'recipes': recipes,
        }
    )

def category(request, category_id):
    recipes = get_list_or_404(
        Recipe.objects.filter(
            category__id=category_id, 
            is_published=True
        ).order_by('-id')
    )

    return render(
        request, 
        'recipes/pages/category.html', 
        context={
            'recipes': recipes,
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
        Q(title__icontains=search_term) | 
        Q(description__icontains=search_term),
        is_published=True,
    ).order_by('-id')

    return render(
        request, 
        'recipes/pages/search.html', 
        context={
            'page_title': f'Search for "{search_term}" | ',
            'search_term': search_term,
            'recipes': recipes,
        }
    )
