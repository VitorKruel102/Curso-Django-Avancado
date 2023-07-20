from django.urls import resolve, reverse

from recipes import views
from recipes.tests.test_recipes_base import RecipeTestBase


class RecipeViewsTest(RecipeTestBase):
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
        # Need a recipe for this test
        self.make_recipe()

        response = self.client.get(reverse('recipes:home'))
        response_context_recipes = response.context['recipes']
        content = response.content.decode('utf-8')

        # Check if one recipe exists
        self.assertIn('Recipe Title', content)
        self.assertEqual(len(response_context_recipes), 1)













   # Testando View Category
    def test_recipes_category_view_function_is_correct(self):
        view = resolve(reverse('recipes:category',
                       kwargs={'category_id': 100000}))
        self.assertIs(view.func, views.category)

    def test_recipes_category_view_returns_404_if_no_recipes_found(self):
        response = self.client.get(
            reverse('recipes:category', kwargs={'category_id': 100000}))
        self.assertEqual(response.status_code, 404)

    def test_recipes_category_template_loads_recipes(self):
        needed_title = 'This is a category test'
        # Need a recipe for this test
        self.make_recipe(title=needed_title)

        response = self.client.get(reverse('recipes:category', kwargs={'category_id':1}))
        response_context_recipes = response.context['recipes']
        content = response.content.decode('utf-8')

        # Check if one recipe exists
        self.assertIn(needed_title, content)











    # Testando View Recipe
    def test_recipes_recipe_view_function_is_correct(self):
        view = resolve(reverse('recipes:recipe', kwargs={'id': 1}))
        self.assertIs(view.func, views.recipe)

    def test_recipes_recipe_view_returns_404_if_no_recipes_found(self):
        response = self.client.get(
            reverse('recipes:recipe', kwargs={'id': 100000}))
        self.assertEqual(response.status_code, 404)

    def test_recipes_recipe_template_loads_the_correct_recipes(self):
        needed_title = 'This is a detail page - It load one recipe'

        # Need a recipe for this test
        self.make_recipe(title=needed_title)

        response = self.client.get(reverse('recipes:recipe', kwargs={'id':1}))
        content = response.content.decode('utf-8')

        # Check if one recipe exists
        self.assertIn(needed_title, content)
