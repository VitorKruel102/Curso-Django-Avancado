from recipes.serializers import RecipeSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response

from ..models import Recipe


@api_view()
def recipe_api_list(request) -> Response:
    recipes = Recipe.objects.get_published()[:10]
    serializer = RecipeSerializer(instance=recipes, many=True)
    return Response(serializer.data)


@api_view()
def recipe_api_detail(request, pk) -> Response:
    recipe = Recipe.objects.filter(pk=pk).first()

    if recipe:
        serializer = RecipeSerializer(instance=recipe, many=False)
        return Response(serializer.data)
    return Response(
        {
          'detail': 'Não Encontrado'
        }, 
        status=418
    )
