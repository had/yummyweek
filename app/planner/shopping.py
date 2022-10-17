from collections import defaultdict
from pprint import pprint

from .models import Suggestion
from .suggestions_dao import get_or_create_suggestions
from ..meals.meal_dao import RecipesDB, get_ingredient_per_category


def get_categorized_shoppinglist(date_, duration) -> dict[str, list[(str, str)]]:
    suggestions: list[Suggestion] = get_or_create_suggestions(date_, duration)
    recipes_db = RecipesDB()
    ingr_list: dict[str, str] = recipes_db.ingredients_for_meals([s.suggestion for s in suggestions])
    ingredient_grouped = defaultdict(list)
    ingredient_per_category = get_ingredient_per_category()
    for k, v in ingr_list.items():
        ingredient_grouped[ingredient_per_category[k].category].append((k, v))
    return ingredient_grouped
