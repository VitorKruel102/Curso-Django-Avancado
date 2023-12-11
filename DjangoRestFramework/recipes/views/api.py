from django.shortcuts import get_object_or_404
from recipes.serializers import RecipeSerializer, TagSerializer
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from tag.models import Tag

from ..models import Recipe


@api_view(http_method_names=['get', 'post'])
def recipe_api_list(request) -> Response:
    if request.method == 'GET':
        recipes = Recipe.objects.get_published()[:10]
        serializer = RecipeSerializer(
            instance=recipes,
            many=True,
            context={'request': request}
        )
        return Response(serializer.data)
    elif request.method == 'POST':
        return Response('POST', status=status.HTTP_201_CREATED)


@api_view()
def recipe_api_detail(request, pk) -> Response:
    recipe = Recipe.objects.filter(pk=pk).first()

    if recipe:
        serializer = RecipeSerializer(
            instance=recipe,
            many=False,
            context={'request': request},
        )
        return Response(serializer.data)
    return Response(
        {
            'detail': 'Não Encontrado'
        },
        status=418
    )


@api_view()
def tag_api_detail(request, pk):
    tag = get_object_or_404(
        Tag.objects.all(),
        pk=pk
    )
    serializer = TagSerializer(
        instance=tag,
        many=False,
        context={'request': request},
    )
    return Response(serializer.data)
