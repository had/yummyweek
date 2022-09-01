from collections import defaultdict
from pprint import pprint

from .suggestions_dao import get_or_create_suggestions
from ..meals.meal_dao import RecipesDB, get_ingredient_per_category


def get_categorized_shoppinglist(date_, duration):
    suggestions = get_or_create_suggestions(date_, duration)
    recipesDB = RecipesDB()
    ingr_list = recipesDB.ingredients_for_meals([s.suggestion for s in suggestions])
    ingredient_grouped = defaultdict(list)
    ingredient_per_category = get_ingredient_per_category()
    for k, v in ingr_list.items():
        ingredient_grouped[ingredient_per_category[k].category].append((k, v))
    pprint(ingredient_grouped)
    return ingredient_grouped