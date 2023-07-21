from .test_recipes_base import RecipeTestBase, Recipe

from django.core.exceptions import ValidationError
from parameterized import parameterized


class RecipeCategoryModelTest(RecipeTestBase):
    def setUp(self) -> None:
        """Inicializa sempre antes do teste."""
        self.category = self.make_category()
        return super().setUp

    def test_recipe_category_name_max_length(self):
        self.category.name = 'A' * 66

        with self.assertRaises(ValidationError):
            self.category.full_clean()

    def test_recipe_category_string_representatio_is_name_field(self):
        needed = 'Testing Representation'

        self.category.name = needed
        self.category.full_clean()
        self.category.save()

        self.assertEqual(
            str(self.category), needed,
            msg=f'Category string representation must be'
                f'"{needed}" but "{str(self.category)}" was received'
        )