from django.urls import resolve, reverse

from recipes import views
from recipes.tests.test_recipes_base import RecipeTestBase


class RecipeViewsSearchTest(RecipeTestBase):
    def test_recipes_search_uses_correct_view_function(self):
        view = resolve(reverse('recipes:search'))
        self.assertIs(view.func, views.search)
    
    def test_recipes_home_view_loads_correct_template(self):
        response = self.client.get(reverse('recipes:search'))
        self.assertTemplateUsed(response, 'recipes/pages/search.html')


    # def test_recipes_home_view_returns_status_code_200_ok(self):
    #     response = self.client.get(reverse('recipes:home'))
    #     self.assertEqual(response.status_code, 200)

    # def test_recipes_home_view_loads_correct_template(self):
    #     response = self.client.get(reverse('recipes:home'))
    #     self.assertTemplateUsed(response, 'recipes/pages/home.html')

    # def test_recipes_home_template_shows_no_recipes_found_if_no_recipes(self):
    #     response = self.client.get(reverse('recipes:home'))
    #     self.assertIn('No recipes found here', response.content.decode('utf-8'))

    # def test_recipes_home_template_loads_recipes(self):
    #     # Need a recipe for this test
    #     self.make_recipe()

    #     response = self.client.get(reverse('recipes:home'))
    #     response_context_recipes = response.context['recipes']
    #     content = response.content.decode('utf-8')

    #     # Check if one recipe exists
    #     self.assertIn('Recipe Title', content)
    #     self.assertEqual(len(response_context_recipes), 1)

    # def test_recipes_home_template_dont_load_recipes_not_published(self):
    #     """Teste recipe is_published False dont show."""
    #     # Need a recipe for this test
    #     self.make_recipe(is_published=False)

    #     response = self.client.get(reverse('recipes:home'))

    #     self.assertIn('No recipes found here', response.content.decode('utf-8'))
