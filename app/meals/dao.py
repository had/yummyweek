from sqlalchemy.exc import IntegrityError

from .models import MealType, Dish, Ingredient
from itertools import product
from collections import defaultdict


class MealsDBAccess:
    @staticmethod
    def get_dishes() -> list[Dish]:
        return Dish.query.all()

    @staticmethod
    def get_ingredients() -> list[Ingredient]:
        return Ingredient.query.all()

    @staticmethod
    def add_all_dishes(db, dishes: list[Dish]) -> int:
        added = 0
        for d in dishes:
            try:
                db.session.add(d)
                db.session.commit()
                added += 1
            except IntegrityError as e:
                db.session.rollback()
        return added

    @staticmethod
    def add_all_ingredients(db, ingredients: list[Ingredient]) -> int:
        added = 0
        for i in ingredients:
            try:
                db.session.add(i)
                db.session.commit()
                added += 1
            except IntegrityError as e:
                print("ADD_ALL_INGREDIENT ERROR ", e)
                db.session.rollback()
        return added


meal_retriever = MealsDBAccess()
ingredients_retriever = MealsDBAccess()


# TODO: change this ugly setter (used for testing purpose) with DI or similar
def change_meal_retriever(mr):
    global meal_retriever
    meal_retriever = mr


def get_dish_dict() -> dict[str, Dish]:
    all_dishes: list[Dish] = meal_retriever.get_dishes()
    return {d.id: d for d in all_dishes}


def get_ingredient_per_category() -> dict[str, str]:
    ingredients = ingredients_retriever.get_ingredients()
    return {i.name: i.category for i in ingredients}


class ComposedMeal:
    def __init__(self, dishes: list[Dish], meal_type: MealType = MealType.both):
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
    all_dishes = meal_retriever.get_dishes()
    return construct_meals_from_dishes(all_dishes)


def get_dish_names() -> dict[str, str]:
    all_dishes = meal_retriever.get_dishes()
    result = {k: v.name for k, v in construct_meals_from_dishes(all_dishes).items()}
    result.update({d.id: d.name for d in all_dishes})
    return result
