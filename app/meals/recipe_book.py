from itertools import groupby

from more_itertools import partition

from app.meals.dao import ComposedMeal
from app.meals.models import Dish


def ingredients_for_meals(meals: list[ComposedMeal]) -> dict[str, str]:
    def parse_ingredients(ingredients_str) -> list[str]:
        ingredient_list = ingredients_str.split("|") if ingredients_str else []
        return ingredient_list

    dishes: list[Dish] = [d for m in meals for d in m.dishes]
    ingredients: list[str] = [i for d in dishes for i in parse_ingredients(d.ingredients)]
    uncountable_ingredients, countable_ingredients = partition(lambda i: "*" in i, ingredients)
    result = {ingredient: "" for ingredient in uncountable_ingredients}

    # aggregate countable ingredients (with "*" in the string)
    # for ex. "potatoes*300 g" and "potatoes*500 g" should result in "potatoes: 800 g"
    # if there are several types like "eggplant*2" and "eggplant*300 g" it
    # should return "eggplant: 2 unit and 300 g"
    # TODO: handle singular vs. plural nouns
    grouped_ingredients = groupby(sorted([i.split("*") for i in countable_ingredients]), key=lambda x: x[0])
    for ingredient, counters_gr in grouped_ingredients:
        parsed_counters = []
        counters = [c[1] for c in counters_gr]
        for c in counters:
            if " " in c:
                parsed_counters.append(c.split(" ")[::-1])  # we reverse the list because we want units first
            else:
                # add fake unit when none is provided
                parsed_counters.append(["", c])
        aggregated_counters = []
        for key, pc_gr in groupby(sorted(parsed_counters), key=lambda c: c[0]):
            pc = [c[1] for c in pc_gr]
            aggregation = sum(map(int, pc))
            aggregated_counters.append(f"{aggregation} {key}")
        result[ingredient] = ' and '.join(aggregated_counters).strip()
    return result
