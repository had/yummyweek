from itertools import groupby

from more_itertools import partition

from app.meals.dao import ComposedMeal
from app.meals.models import Dish, DishIngredient


def ingredients_for_meals(meals: list[ComposedMeal]) -> dict[str, str]:
    def parse_ingredients(ingredients_str) -> list[str]:
        ingredient_list = ingredients_str.split("|") if ingredients_str else []
        return ingredient_list

    dishes: list[Dish] = [d for m in meals for d in m.dishes]
    ingredients: list[DishIngredient] = [i for d in dishes for i in d.ingredients]
    countable_di, uncountable_di = partition(lambda di: di.quantity is None, ingredients)
    result: dict[str, str] = {di.ingredient.name: "" for di in uncountable_di}

    # aggregate countable ingredients (with a quantity)
    # for ex. "potatoes,300,g" and "potatoes,500,g" should result in "potatoes: 800 g"
    # if there are several types like "eggplant,2" and "eggplant,300,g" it
    # should return "eggplant: 2 unit and 300 g"
    # TODO: handle singular vs. plural nouns
    grouped_ingredients = groupby(sorted(countable_di, key=lambda di: di.ingredient.name), key=lambda di: di.ingredient.name)
    for ingredient, counters_gr in grouped_ingredients:
        counters = [(di.unit if di.unit else "", di.quantity) for di in counters_gr]
        aggregated_counters = []
        # group by unit
        for unit, quantities in groupby(sorted(counters), key=lambda c: c[0]):
            aggregation = sum([int(c[1]) for c in quantities])
            aggregated_counters.append(f"{aggregation} {unit}")
        result[ingredient] = ' and '.join(aggregated_counters).strip()
    return result
