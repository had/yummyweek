import pytest

from app import create_app, db
from app.meals.dao import ComposedMeal
from app.meals.recipe_book import ingredients_for_meals
from app.meals.models import Dish, Ingredient


@pytest.fixture()
def test_db():
    app = create_app("testing")
    app_context = app.app_context()
    app_context.push()
    db.create_all()
    yield db
    db.session.remove()
    db.drop_all()
    app_context.pop()

@pytest.fixture()
def roman_ingredients(test_db):
    ingredients = ["eggs", "milk", "honey", "olive oil", "chicken", "flour"]
    test_db.session.add_all([Ingredient(name=i) for i in ingredients])
    test_db.session.commit()


# Taken from https://delishably.com/world-cuisine/ancient-food-rome
@pytest.fixture()
def eggs_with_honey(roman_ingredients):
    ingredients = Dish.parse_ingredients("eggs*4|milk*275 ml|honey*3 tbsp|olive oil*1 tbsp")
    return Dish(id="EGGS_WITH_HONEY", name="Eggs with honey",
             category="Lunch", prep_time_m=30, cooking_time_m=25, periodicity_d=7,
             ingredients=ingredients)


@pytest.fixture()
def dormouse(roman_ingredients):
    ingredients = Dish.parse_ingredients("chicken*8 drumsticks|honey*1 tbsp|flour*1 cup")
    return Dish(id="DORMOUSE", name="Something probably delicious",
             category="Lunch", prep_time_m=20, cooking_time_m=0, periodicity_d=1,
             ingredients=ingredients)


def test_ingredient_1_recipe(eggs_with_honey):
    ingr = ingredients_for_meals([ComposedMeal([eggs_with_honey])])
    assert ingr == {"eggs": "4", "milk": "275 ml", "honey": "3 tbsp", "olive oil": "1 tbsp"}


def test_ingredient_aggregate_2_recipes(eggs_with_honey, dormouse):
    ingr = ingredients_for_meals([ComposedMeal([d]) for d in [eggs_with_honey, dormouse]])
    assert ingr["honey"] == "4 tbsp"

# TODO: more test cases and dev to cover more mixed situations properly
