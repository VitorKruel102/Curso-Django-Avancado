from pyexpat import model
from attr import field
from rest_framework import serializers
from tag.models import Tag

from .models import Category, Recipe


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name', 'slug']

    # id = serializers.IntegerField()
    # name = serializers.CharField(max_length=255)
    # slug = serializers.SlugField()


class RecipeSerializer(serializers.Serializer):
    
    class Meta:
        model = Recipe
        fields = [
            'id', 
            'title',
            'description',
            'author',
            'category',
            'tags',
            'public',
            'preparation',
            'tag_objects',
            'tag_links',
        ]

    public = serializers.BooleanField(source='is_published', read_only=True)
    preparation = serializers.SerializerMethodField(read_only=True)
    category_name = serializers.StringRelatedField(source='category')
    author = serializers.StringRelatedField()
    tag_objects = TagSerializer(
        many=True, 
        source='tags', 
        read_only=True,
    )
    tag_links = serializers.HyperlinkedRelatedField(
        many=True,
        source='tags',
        view_name='recipes:recipes_api_v2_tag',
        read_only=True,
    )

    def get_preparation(self, recipe):
        return f'{recipe.preparation_time} {recipe.preparation_time_unit}'
