import pytest

from app.meals.dao import change_meal_retriever
from app.meals.recipe_book import RecipeBook
from app.meals.models import Recipe, Dish
from tests import FakeMealRetriever


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
    roman_banquet_dishes = [
        Dish(id="EGGS_WITH_HONEY", name="Eggs with honey",
             category="Lunch", prep_time_m=30, cooking_time_m=25, periodicity_d=7),
        Dish(id="DORMOUSE", name="Something probably delicious",
             category="Lunch", prep_time_m=20, cooking_time_m=0, periodicity_d=1),
    ]
    change_meal_retriever(FakeMealRetriever(roman_banquet_dishes))
    recipes = RecipeBook(recipes=roman_recipes)
    ingr = recipes.ingredients_for_meals(["EGGS_WITH_HONEY"])
    assert ingr == {"eggs": "4", "milk": "275 ml", "honey": "3 tbsp", "olive oil": "1 tbsp"}


def test_ingredient_aggregate_2_recipes(roman_recipes):
    recipes = RecipeBook(recipes=roman_recipes)
    ingr = recipes.ingredients_for_meals(["EGGS_WITH_HONEY", "DORMOUSE"])
    assert ingr["honey"] == "4 tbsp"

# TODO: more test cases and dev to cover more mixed situations properly
