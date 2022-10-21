from cachetools.func import ttl_cache

from .models import MealType, Recipe, Ingredient, Dish
import os
from itertools import groupby, product
from more_itertools import partition
from collections import defaultdict

mock_food_env = os.environ.get('YUMMYWEEK_XLS')


def read_mock_recipes(path):
    import pandas as pd
    import numpy as np
    recipes = []
    recipes_df = pd.read_excel(path, sheet_name="food_recipes").replace({np.nan: None})
    for _, row in recipes_df.iterrows():
        d = row.to_dict()
        recipes.append(Recipe(**d))
    return recipes


mock_recipes = read_mock_recipes(mock_food_env) if mock_food_env else {}


def read_mock_ingredient_per_categories(path):
    import pandas as pd
    import numpy as np
    ingredients_per_category = {}
    ingredients_df = pd.read_excel(path, sheet_name="food_ingredients_categories").replace({np.nan: None})
    for _, row in ingredients_df.iterrows():
        d = row.to_dict()
        ingredients_per_category[d["ingredient"]] = Ingredient(id=d["ingredient"], category=d["category"])
    return ingredients_per_category


mock_ingredient_per_category = read_mock_ingredient_per_categories(mock_food_env) if mock_food_env else {}


def get_recipes():
    return mock_recipes


def get_ingredient_per_category():
    return mock_ingredient_per_category


class RecipesDB:
    def __init__(self, recipes=None):
        def parse_ingredients(ingredients_str) -> list[str]:
            ingredient_list = ingredients_str.split("|") if ingredients_str else []
            return ingredient_list

        recipes = recipes or get_recipes()
        self.recipes_ingredients = {r.id: parse_ingredients(r.ingredients) for r in recipes}

    def ingredients_for_meals(self, meals: list[str]) -> dict[str, str]:
        dishes: list[Dish] = [d for m in meals for d in ComposedMeal.from_composed_id(m).dishes]
        ingredients = [i for d in dishes for i in self.recipes_ingredients.get(d.id, [])]
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


class XlsxDishReader:
    def __init__(self, path):
        self.path = path

    def to_list(self) -> list[Dish]:
        import pandas as pd
        import numpy as np

        print("Reading XLSX spreadsheet " + self.path)
        dishes_df = pd.read_excel(self.path, sheet_name="food_dishes").replace({np.nan: None})
        dishes = []
        for _, row in dishes_df.iterrows():
            d = row.to_dict()
            if d['active'] != 'Y':
                continue
            del d['active']
            dishes.append(Dish(**d))
        return dishes

    @ttl_cache(maxsize=1, ttl=300)
    def get(self) -> list[Dish]:
        return self.to_list()


class DBDishReader:
    @staticmethod
    def get() -> list[Dish]:
        return Dish.query.all()


meal_retriever = DBDishReader()


# TODO: change this ugly setter (used for testing purpose) with DI or similar
def change_meal_retriever(mr):
    global meal_retriever
    meal_retriever = mr


def get_dish_dict() -> dict[str, Dish]:
    all_dishes: list[Dish] = meal_retriever.get()
    return {d.id: d for d in all_dishes}


class ComposedMeal:
    def __init__(self, dishes: list[Dish], meal_type: MealType):
        self.dishes = dishes
        self.id = "+".join([d.id for d in dishes])
        self.name = ' & '.join([d.name for d in dishes])
        self.prep_time_m = sum([d.prep_time_m for d in dishes])
        self.cooking_time_m = sum([d.cooking_time_m for d in dishes])
        self.periodicity_d = max([d.periodicity_d for d in dishes])
        self.meal_moment = meal_type

    # TODO needing MealType here is not ideal, find a way to get rid of it
    @classmethod
    def from_composed_id(cls, composed_id: str, meal_type: MealType = MealType.both):
        dish_dict = get_dish_dict()
        dishes = [dish_dict[c] for c in composed_id.split("+")]
        return cls(dishes, meal_type)


def construct_meals_from_dishes(dishes: list[Dish]) -> dict[str, ComposedMeal]:
    dishes_by_type = defaultdict(list)
    results: dict[str, ComposedMeal] = {}
    meal_templates = []
    for d in dishes:
        if d.category.lower() not in ["lunch", "dinner", "both"]:
            dishes_by_type[d.category].append(d)
        else:
            if not d.elements:
                # this dish can be a full meal (no sub elements)
                results[d.id] = ComposedMeal([d], MealType(d.category))
            else:
                # keep this for a second pass
                meal_templates.append(d)

    # second pass: compose meals
    for template in meal_templates:
        elt_types = template.elements.split(';')
        meal_dishes = [dishes_by_type[t] for t in elt_types]
        composed_meals = product(*meal_dishes)
        for cm in composed_meals:
            meal = ComposedMeal(cm, MealType(template.category))
            results[meal.id] = meal
    return results


def get_all_meals() -> dict[str, ComposedMeal]:
    all_dishes = meal_retriever.get()
    return construct_meals_from_dishes(all_dishes)


def get_dish_names() -> dict[str, str]:
    all_dishes = meal_retriever.get()
    result = {k: v.name for k, v in construct_meals_from_dishes(all_dishes).items()}
    result.update({d.id: d.name for d in all_dishes})
    return result
