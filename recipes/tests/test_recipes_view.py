from django.test import TestCase
from django.urls import resolve, reverse

from recipes import views
from recipes.models import Category, Recipe, User


class RecipeViewsTest(TestCase):
    # Testando View Home
    def test_recipes_home_view_function_is_correct(self):
        view = resolve(reverse('recipes:home'))
        self.assertIs(view.func, views.home)
    
    def test_recipes_home_view_returns_status_code_200_ok(self):
        response = self.client.get(reverse('recipes:home'))
        self.assertEqual(response.status_code, 200)

    def test_recipes_home_view_loads_correct_template(self):
        response = self.client.get(reverse('recipes:home'))
        self.assertTemplateUsed(response, 'recipes/pages/home.html')

    def test_recipes_home_template_shows_no_recipes_found_if_no_recipes(self):
        """
        response.content - Retorna o Template 
        response.content.decode('utf-8') - Transforma em UTF-8
        """
        response = self.client.get(reverse('recipes:home'))
        self.assertIn('No recipes found here', response.content.decode('utf-8'))
   
    def test_recipes_home_template_loads_recipes(self):
        category = Category.objects.create(name='Category')
        assert 1 == 1

   # Testando View Category
    def test_recipes_category_view_function_is_correct(self):
        view = resolve(reverse('recipes:category', kwargs={'category_id': 100000}))
        self.assertIs(view.func, views.category)

    def test_recipes_category_view_returns_404_if_no_recipes_found(self):
        response = self.client.get(reverse('recipes:category', kwargs={'category_id': 100000}))
        self.assertEqual(response.status_code, 404)

    # Testando View Recipe
    def test_recipes_recipe_view_function_is_correct(self):
        view = resolve(reverse('recipes:recipe', kwargs={'id': 1}))
        self.assertIs(view.func, views.recipe)

    def test_recipes_recipe_view_returns_404_if_no_recipes_found(self):
        response = self.client.get(reverse('recipes:recipe', kwargs={'id': 100000}))
        self.assertEqual(response.status_code, 404)

