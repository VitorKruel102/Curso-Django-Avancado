from django.contrib import admin
from .models import Category, Recipe


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    ...


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'created_at', 'is_published', 'author')
    list_display_links = ('title', 'created_at')
    list_filter = ('category', 'author', 'is_published')
    search_fields = ('id', 'title', 'descriptions', 'slug', 'preparations_steps')
    list_per_page = 10
    list_editable = ['is_published']
    ordering = ['id']