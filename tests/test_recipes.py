import pytest

from app.meals.meal_dao import RecipesDB
from app.meals.models import Recipe


@pytest.fixture()
def roman_recipes():
    mock_recipes = [
        # Taken from https://delishably.com/world-cuisine/ancient-food-rome
        Recipe(id="EGGS_WITH_HONEY", ingredients="eggs*4|milk*275 ml|honey*3 tbsp|olive oil*1 tbsp"),
        Recipe(id="DORMOUSE", ingredients="chicken*8 drumsticks|honey*1 tbsp|flour*1 cup"),
        Recipe(id="GLOBULI", ingredients="curd cheese*500 g|honey|olive oil"),
        Recipe(id="LIBUM", ingredients="flour*1/2 cup|egg*1")
    ]
    return mock_recipes

def test_ingredient_1_recipe(roman_recipes):
    recipes = RecipesDB(recipes=roman_recipes)
    ingr = recipes.ingredients_for_meals(["EGGS_WITH_HONEY"])
    assert ingr == {"eggs": "4", "milk": "275 ml", "honey": "3 tbsp", "olive oil": "1 tbsp"}

def test_ingredient_aggregate_2_recipes(roman_recipes):
    recipes = RecipesDB(recipes=roman_recipes)
    ingr = recipes.ingredients_for_meals(["EGGS_WITH_HONEY", "DORMOUSE"])
    assert ingr["honey"] == "4 tbsp"

# TODO: more test cases and dev to cover more mixed situations properly
