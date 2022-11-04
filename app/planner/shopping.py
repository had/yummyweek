from collections import defaultdict

from .models import Suggestion
from .suggestions_dao import get_or_create_suggestions
from ..meals.dao import get_ingredient_per_category, ComposedMeal
from ..meals.recipe_book import ingredients_for_meals


def get_categorized_shoppinglist(date_, duration) -> dict[str, list[(str, str)]]:
    suggestions: list[Suggestion] = get_or_create_suggestions(date_, duration)
    committed_suggestions: list[ComposedMeal] =\
        [ComposedMeal.from_composed_id(s.suggestion) for s in suggestions if s.committed]
    ingredient_list: dict[str, str] = ingredients_for_meals(committed_suggestions)
    ingredient_grouped = defaultdict(list)
    ingredient_per_category = get_ingredient_per_category()
    for k, v in ingredient_list.items():
        ingredient_grouped[ingredient_per_category[k]].append((k, v))
    return ingredient_grouped
