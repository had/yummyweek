from app.meals.meal_dao import ComposedMeal, change_meal_retriever, construct_meals_from_dishes
from app.meals.models import Dish, MealType
from datetime import date

from app.planner.meal_planning import MealPlanner

class FakeMealRetriever:
    def __init__(self, dishes):
        self.dishes = dishes

    def get(self):
        return self.dishes

def test_planner_history():
    roman_banquet_dishes = [
        # names from https://delishably.com/world-cuisine/ancient-food-rome
        Dish(id="TEST_FOOD_1", name="Boiled ostrich with sweet sauce",
             category="Lunch", prep_time_m=50, cooking_time_m=100, periodicity_d=3),
        Dish(id="TEST_FOOD_2", name="Turtledove boiled in its feathers",
             category="Lunch", prep_time_m=90, cooking_time_m=60, periodicity_d=5),
        Dish(id="TEST_FOOD_3", name="Flamingo boiled with dates",
             category="Lunch", prep_time_m=120, cooking_time_m=45, periodicity_d=2),
        Dish(id="TEST_FOOD_4", name="Sea urchins with spices, honey, oil, and egg sauce",
             category="Lunch", prep_time_m=30, cooking_time_m=25, periodicity_d=7),
        Dish(id="TEST_FOOD_5", name="Pitted dates stuffed with nuts and pine kernels, fried in honey",
             category="Lunch", prep_time_m=20, cooking_time_m=0, periodicity_d=1),
    ]
    change_meal_retriever(FakeMealRetriever(roman_banquet_dishes))
    meals = construct_meals_from_dishes(roman_banquet_dishes)
    history = {
        date(68, 6, 3): [ComposedMeal.from_composed_id("TEST_FOOD_1", MealType.lunch),
                         ComposedMeal.from_composed_id("TEST_FOOD_2", MealType.lunch)
                         ],
        date(68, 6, 4): [ComposedMeal.from_composed_id("TEST_FOOD_3", MealType.lunch),
                         ComposedMeal.from_composed_id("TEST_FOOD_4", MealType.lunch),
                         ],
    }
    planner = MealPlanner(date_from=date(68, 6, 5), meals=meals, history=history)
    assert planner.max_periodicity == 7
    assert planner.not_before_table["TEST_FOOD_1"] == date(68, 6, 6)
    assert planner.not_before_table["TEST_FOOD_2"] == date(68, 6, 8)
    assert planner.not_before_table["TEST_FOOD_3"] == date(68, 6, 6)
    assert planner.not_before_table["TEST_FOOD_4"] == date(68, 6, 11)
    suggestions = planner.get_eligible_meals(date(68, 6, 6))
    assert [s.id for s in suggestions] == ["TEST_FOOD_1", "TEST_FOOD_3", "TEST_FOOD_5"]


def test_planner_history_compounded():
    roman_banquet_dishes = [
        # names from https://delishably.com/world-cuisine/ancient-food-rome
        Dish(id="TEST_ELEMENT_1", name="Jellyfish and eggs",
             category="appetiser", prep_time_m=10, cooking_time_m=20, periodicity_d=3),
        Dish(id="TEST_ELEMENT_2", name="Sea urchins with spices, honey, oil, and egg sauce",
             category="appetiser", prep_time_m=10, cooking_time_m=20, periodicity_d=3),
        Dish(id="TEST_ELEMENT_3", name="Roast parrot",
             category="main_course", prep_time_m=10, cooking_time_m=20, periodicity_d=10),
        Dish(id="TEST_ELEMENT_4", name="Flamingo boiled with dates",
             category="main_course", prep_time_m=10, cooking_time_m=20, periodicity_d=3),
        Dish(id="TEST_FOOD_1", name="Boiled ostrich with sweet sauce",
             category="Lunch", prep_time_m=10, cooking_time_m=20, periodicity_d=3),
        Dish(id="TEST_FOOD_2", name="Turtledove boiled in its feathers",
             category="Dinner", prep_time_m=10, cooking_time_m=20, periodicity_d=5),
        Dish(id="TEST_FOOD_3", name="Pitted dates stuffed with nuts and pine kernels, fried in honey",
             category="Both", prep_time_m=10, cooking_time_m=20, periodicity_d=3),
        Dish(id="COMPOUNDED_1", name="Ancient Rome Menu",
             category="Lunch", elements="appetiser;main_course")
    ]
    change_meal_retriever(FakeMealRetriever(roman_banquet_dishes))
    meals = construct_meals_from_dishes(roman_banquet_dishes)
    history = {
        date(68, 6, 3): [
            ComposedMeal.from_composed_id("TEST_ELEMENT_1+TEST_ELEMENT_4", MealType.lunch),
            ComposedMeal.from_composed_id("TEST_FOOD_2", MealType.dinner)],
        date(68, 6, 4): [ComposedMeal.from_composed_id("TEST_FOOD_3", MealType.lunch)],
    }
    planner = MealPlanner(date_from=date(68, 6, 5), meals=meals, history=history)
    assert planner.max_periodicity == 10
    suggestions = [s.id for s in planner.get_eligible_meals(date(68, 6, 5))]
    assert "TEST_ELEMENT_1+TEST_ELEMENT_3" not in suggestions
    assert "TEST_ELEMENT_2+TEST_ELEMENT_3" in suggestions


def test_planner_history_element():
    roman_banquet_dishes = [
        # names from https://delishably.com/world-cuisine/ancient-food-rome
        Dish(id="TEST_ELEMENT_1", name="Jellyfish and eggs",
             category="appetiser", prep_time_m=10, cooking_time_m=20, periodicity_d=3),
        Dish(id="TEST_ELEMENT_2", name="Sea urchins with spices, honey, oil, and egg sauce",
             category="appetiser", prep_time_m=10, cooking_time_m=20, periodicity_d=3),
        Dish(id="TEST_ELEMENT_3", name="Roast parrot",
             category="main_course", prep_time_m=10, cooking_time_m=20, periodicity_d=10),
        Dish(id="COMPOUNDED_1", name="Ancient Rome Menu",
             category="Lunch", elements="appetiser;main_course")
    ]
    change_meal_retriever(FakeMealRetriever(roman_banquet_dishes))
    meals = construct_meals_from_dishes(roman_banquet_dishes)
    history = {
        date(68, 6, 3): [ComposedMeal.from_composed_id("TEST_ELEMENT_1", MealType.lunch)],
    }
    planner = MealPlanner(date_from=date(68, 6, 4), meals=meals, history=history)
    suggestions = [s.id for s in planner.get_eligible_meals(date(68, 6, 4))]
    assert suggestions == ["TEST_ELEMENT_2+TEST_ELEMENT_3"]
