from .models import Meal, MealType, MealElement, Recipe
import os
import itertools
from more_itertools import partition
from collections import defaultdict

checks = ["periodicity_d", "prep_time_m", "cooking_time_m"]


def sanity_check(m):
    if isinstance(m, Meal) and (getattr(m, "elements") or "BATCH" in (m.tags or "")):
        # if it's a meal and has elements or is for batch cooking, skip checks
        return True
    warn = ""
    for check in checks:
        if getattr(m, check) is None:
            warn += f" missing {check};"
    if warn:
        print(f"* Warning: {m.id}{warn}")
        return False
    return True


def read_mock_food(path):
    import pandas as pd
    import numpy as np
    print(f"Using mock food data from {path}")

    elements = []
    food_df = pd.read_excel(path, sheet_name="food_elements").replace({np.nan: None})
    for _, row in food_df.iterrows():
        d = row.to_dict()
        if d['active'] != 'Y':
            continue
        del d['active']
        elements.append(MealElement(**d))
    print(f"Found {len(elements)} meals")

    meals = []
    food_df = pd.read_excel(path, sheet_name="food_meals").replace({np.nan: None})
    for _, row in food_df.iterrows():
        d = row.to_dict()
        if d['active'] != 'Y':
            continue
        del d['active']
        d['meal_type'] = MealType(d['meal_type'])
        meals.append(Meal(**d))
    print(f"Found {len(meals)} meals")

    return list(filter(sanity_check, elements)), list(filter(sanity_check, meals))


def generate_available_meals(elements, meals):
    elements_by_type = defaultdict(list)
    for e in elements:
        elements_by_type[e.category].append(e)
    result = {}
    # create compounded meals
    for m in meals:
        if m.elements:
            elt_types = m.elements.split(';')
            meal_elements = [elements_by_type[t] for t in elt_types]
            compounded_meals = itertools.product(*meal_elements)
            for cm in compounded_meals:
                id_ = '+'.join([e.id for e in cm])
                name = ' & '.join([e.name for e in cm])
                prep_time = sum([e.prep_time_m for e in cm])
                cooking_time = sum([e.cooking_time_m for e in cm])
                periodicity = max([e.periodicity_d for e in cm])
                meal_type = MealType(m.meal_type)
                result[id_] = Meal(id=id_, name=name, meal_type=meal_type, prep_time_m=prep_time,
                                   cooking_time_m=cooking_time, periodicity_d=periodicity)
        else:
            # simple meal, just add it to the results
            result[m.id] = m
    return result


mock_food_env = os.environ.get('YUMMYWEEK_XLS')
mock_elements, mock_meals = read_mock_food(mock_food_env) if mock_food_env else ([], [
    Meal(id="COURGETTES", name="Courgettes", prep_time_m=20, cooking_time_m=25, meal_type=MealType.dinner,
         periodicity_d=8),
])

mock_meals_2 = generate_available_meals(mock_elements, mock_meals)



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


def get_meal_elements():
    return mock_elements


def get_meals_unprocessed():
    return mock_meals


def get_meals():
    return mock_meals_2


def get_recipes():
    return mock_recipes


class RecipesDB:
    def __init__(self, recipes=None):
        def parse_ingredients(ingredients_str):
            ingr_list = ingredients_str.split("|") if ingredients_str else []
            return ingr_list

        recipes = recipes or get_recipes()
        self.recipes_ingr = {r.id: parse_ingredients(r.ingredients) for r in recipes}


    def ingredients_for_meals(self, meals):
        meals_or_elements = [e for m in meals for e in m.split('+')]
        ingredients = [i for e in meals_or_elements for i in self.recipes_ingr.get(e, [])]
        print(ingredients)
        uncountable_ingr, countable_ingr = partition(lambda i: "*" in i,
                                                     [ingr for e in meals_or_elements for ingr in self.recipes_ingr.get(e, [])])
        processed_ingr = {ingr: "" for ingr in uncountable_ingr}
        # aggregate countable ingredients (with "*" in the string)
        # for ex. "potatoes*300 g" and "potatoes*500 g" should result in "potatoes: 800 g"
        # if there are several types like "egplant*2" and "eggplant*300 g" it should return "eggplant: 2 unit and 300 g"
        # TODO: handle singular vs. plural nouns
        grouped_ingr = itertools.groupby(sorted([i.split("*") for i in countable_ingr]), key=lambda x:x[0])
        for ingr, counters_gr in grouped_ingr:
            parsed_counters = []
            counters = [c[1] for c in counters_gr]
            for c in counters:
                if " " in c:
                    parsed_counters.append(c.split(" ")[::-1]) # we reverse the list because we want units first
                else:
                    # add fake unit when none is provided
                    parsed_counters.append(["",c])
            aggregated_counters = []
            print("^^^ ", ingr, " // ", parsed_counters)
            for key, pc_gr in itertools.groupby(sorted(parsed_counters), key=lambda c: c[0]):
                pc = [c[1] for c in pc_gr]
                aggreg = sum(map(int, pc))
                print(ingr, aggreg, key)
                aggregated_counters.append(f"{aggreg} {key}")
            processed_ingr[ingr] = ' and '.join(aggregated_counters).strip()
        print(processed_ingr)
        return processed_ingr
