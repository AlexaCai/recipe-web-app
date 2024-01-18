from django.test import TestCase
from .models import (
    Recipe,
    RecipeIngredients,
    RecipeCookingInstructions,
    RecipeToolsNeeded,
    RecipeSimilarComplementary,
)

class RecipeModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by some test methods
        recipe = Recipe.objects.create(
            recipe_name="Tacos al pastor",
            is_public=True,
            origin_country="mexican",
            recipe_category="dinner",
            cooking_time=90,
            recipe_estimated_cost=20,
            creation_date="2020-10-10",
            description="Tacos al pastor are a meat-cooking method for tacos that originated in central Mexico, but is popular throughout the country. Although the meat format is reminiscent of that used to make Middle Eastern kebabs or shawarma, the meat is almost exclusively pork.",
            special_note="no special note"
        )

        RecipeIngredients.objects.create(
            recipe=recipe,  
            ingredient_name="tortillas",
            quantity=25,
            possible_substitute="bread",
        )

        RecipeCookingInstructions.objects.create(
            recipe=recipe, 
            step_name="Prepare", 
            step_instruction="Prepare the tortillas"
        )

        RecipeToolsNeeded.objects.create(
            recipe=recipe, 
            cooking_tool_name="spatula"
        )

        RecipeSimilarComplementary.objects.create(
            recipe=recipe,  
            complementary_recipe_name="tacos suadero",
            complementary_recipe_link_unsigned_users='https://www.example1.com',
            complementary_recipe_link_signed_users='https://www.example2.com'
        )

    def test_recipe_name(self):
        # Get a recipe object to test
        recipe = Recipe.objects.get(id=1)
        # Get the metadata for the 'name' field and use it to query its data
        field_label = recipe._meta.get_field("recipe_name").verbose_name
        # Compare the value to the expected result
        self.assertEqual(field_label, "recipe name")

    def test_recipe_name_max_length(self):
        recipe = Recipe.objects.get(id=1)
        max_length = recipe._meta.get_field("recipe_name").max_length
        self.assertEqual(max_length, 50)

    def test_recipe_is_public(self):
        recipe = Recipe.objects.get(id=1)
        is_public = recipe._meta.get_field("is_public")
        self.assertTrue(is_public)

    def test_recipe_cooking_time_data_type(self):
        recipe = Recipe.objects.get(id=1)
        data_type = isinstance(recipe.cooking_time, int)
        self.assertTrue(data_type, int)

    def test_recipe_estimated_cost_data_type(self):
        recipe = Recipe.objects.get(id=1)
        data_type = isinstance(recipe.recipe_estimated_cost, float)
        self.assertTrue(data_type, int)

    def test_calculate_difficulty_easy(self):
        recipe = Recipe(cooking_time=5)
        # Save the recipe so it has a primary key (id)
        recipe.save()
        ingredients = [
            RecipeIngredients(
                recipe=recipe,
                ingredient_name="ingredient1",
                quantity=1
            ),
            RecipeIngredients(
                recipe=recipe,
                ingredient_name="ingredient2",
                quantity=1
            ),
            RecipeIngredients(
                recipe=recipe,
                ingredient_name="ingredient3",
                quantity=1
            )
        ]
        RecipeIngredients.objects.bulk_create(ingredients)
        difficulty = recipe.calculate_difficulty()
        self.assertEqual(difficulty, "easy")


    def test_calculate_difficulty_medium(self):
        recipe = Recipe(cooking_time=5)
        # Save the recipe so it has a primary key (id)
        recipe.save()
        ingredients = [
            RecipeIngredients(
                recipe=recipe,
                ingredient_name="ingredient1",
                quantity=1
            ),
            RecipeIngredients(
                recipe=recipe,
                ingredient_name="ingredient2",
                quantity=1
            ),
            RecipeIngredients(
                recipe=recipe,
                ingredient_name="ingredient3",
                quantity=1
            ),
            RecipeIngredients(
                recipe=recipe,
                ingredient_name="ingredient4",
                quantity=1
            )
        ]
        RecipeIngredients.objects.bulk_create(ingredients)
        difficulty = recipe.calculate_difficulty()
        self.assertEqual(difficulty, "medium")

    def test_calculate_difficulty_intermediate(self):
        recipe = Recipe(cooking_time=35)
        # Save the recipe so it has a primary key (id)
        recipe.save()
        ingredients = [
            RecipeIngredients(
                recipe=recipe,
                ingredient_name="ingredient1",
                quantity=1
            ),
            RecipeIngredients(
                recipe=recipe,
                ingredient_name="ingredient2",
                quantity=1
            ),
            RecipeIngredients(
                recipe=recipe,
                ingredient_name="ingredient3",
                quantity=1
            )
        ]
        RecipeIngredients.objects.bulk_create(ingredients)
        difficulty = recipe.calculate_difficulty()
        self.assertEqual(difficulty, "intermediate")
    

    def test_calculate_difficulty_hard(self):
        recipe = Recipe(cooking_time=35)
        # Save the recipe so it has a primary key (id)
        recipe.save()
        ingredients = [
            RecipeIngredients(
                recipe=recipe,
                ingredient_name="ingredient1",
                quantity=1
            ),
            RecipeIngredients(
                recipe=recipe,
                ingredient_name="ingredient2",
                quantity=1
            ),
            RecipeIngredients(
                recipe=recipe,
                ingredient_name="ingredient3",
                quantity=1
            ),
            RecipeIngredients(
                recipe=recipe,
                ingredient_name="ingredient4",
                quantity=1
            )
        ]
        RecipeIngredients.objects.bulk_create(ingredients)
        difficulty = recipe.calculate_difficulty()
        self.assertEqual(difficulty, "hard")

    def test_get_absolute_url(self):
        recipe = Recipe.objects.get(id=1)
        self.assertEqual(recipe.get_absolute_url(), '/recipes-detail-unsigned-users/1')

    def test_get_absolute_url_signed_users(self):
        recipe = Recipe.objects.get(id=1)
        self.assertEqual(recipe.get_absolute_url_signed_users(), '/recipes-detail-signed-users/1')

    def test_recipe_ingredients_name_max_length(self):
        ingredient = RecipeIngredients.objects.get(recipe_id=1)
        max_length = ingredient._meta.get_field('ingredient_name').max_length
        self.assertEqual(max_length, 100)

    def test_recipe_ingredient_quantity(self):
        ingredient = RecipeIngredients.objects.get(recipe_id=1)
        data_type = isinstance(ingredient.quantity, float)
        self.assertTrue(data_type, float)

    def test_recipe_ingredients_substitute_max_length(self):
        ingredient = RecipeIngredients.objects.get(recipe_id=1)
        max_length = ingredient._meta.get_field('possible_substitute').max_length
        self.assertEqual(max_length, 100)

    def test_recipe_ingredients_substitute_note_max_length(self):
        ingredient = RecipeIngredients.objects.get(recipe_id=1)
        max_length = ingredient._meta.get_field('substitue_special_note').max_length
        self.assertEqual(max_length, 300)

    def test_recipe_instruction_cooking_step(self):
        instruction = RecipeCookingInstructions.objects.get(id=1)
        max_length = instruction._meta.get_field('step_name').max_length
        self.assertEqual(max_length, 100)

    def test_recipe_instruction_cooking_step_instruction(self):
        instruction = RecipeCookingInstructions.objects.get(id=1)
        max_length = instruction._meta.get_field('step_instruction').max_length
        self.assertEqual(max_length, 500)

    def test_recipe_cooking_tool_name(self):
        tool = RecipeToolsNeeded.objects.get(id=1)
        max_length = tool._meta.get_field('cooking_tool_name').max_length
        self.assertEqual(max_length, 100)

    def test_recipe_similar_recipe_name(self):
        similar_recipe = RecipeSimilarComplementary.objects.get(id=1)
        max_length = similar_recipe._meta.get_field('complementary_recipe_name').max_length
        self.assertEqual(max_length, 100)