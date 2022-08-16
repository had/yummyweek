from app.meals.models import Meal, MealElement
from datetime import date

from app.planner.meal_planning import MealPlanner


def test_planner_history():
    roman_banquet_meals = {
        # names from https://delishably.com/world-cuisine/ancient-food-rome
        "TEST_FOOD_1": Meal(id="TEST_FOOD_1", name="Boiled ostrich with sweet sauce", periodicity_d=3),
        "TEST_FOOD_2": Meal(id="TEST_FOOD_2", name="Turtledove boiled in its feathers", periodicity_d=5),
        "TEST_FOOD_3": Meal(id="TEST_FOOD_3", name="Flamingo boiled with dates", periodicity_d=2),
        "TEST_FOOD_4": Meal(id="TEST_FOOD_4", name="Sea urchins with spices, honey, oil, and egg sauce", periodicity_d=7),
        "TEST_FOOD_5": Meal(id="TEST_FOOD_5", name="Pitted dates stuffed with nuts and pine kernels, fried in honey", periodicity_d=1),
    }
    history = {
        date(68, 6, 3): ["TEST_FOOD_1", "TEST_FOOD_2"],
        date(68, 6, 4): ["TEST_FOOD_3", "TEST_FOOD_4"],
    }
    planner = MealPlanner(date_from=date(68, 6, 5), meals=roman_banquet_meals, history=history)
    assert planner.max_periodicity == 7
    assert planner.not_before_table["TEST_FOOD_1"] == date(68, 6, 6)
    assert planner.not_before_table["TEST_FOOD_2"] == date(68, 6, 8)
    assert planner.not_before_table["TEST_FOOD_3"] == date(68, 6, 6)
    assert planner.not_before_table["TEST_FOOD_4"] == date(68, 6, 11)
    suggestions = planner.get_eligible_meals(date(68, 6, 6))
    assert [s.id for s in suggestions] == ["TEST_FOOD_1", "TEST_FOOD_3", "TEST_FOOD_5"]

def test_planner_history_compounded():
    roman_banquet_elements = [
        # names from https://delishably.com/world-cuisine/ancient-food-rome
        MealElement(id="TEST_ELEMENT_1", name="Jellyfish and eggs",
                    category="appetiser", prep_time_m=10, cooking_time_m=20, periodicity_d=3),
        MealElement(id="TEST_ELEMENT_2", name="Sea urchins with spices, honey, oil, and egg sauce",
                    category="appetiser", prep_time_m=10, cooking_time_m=20,  periodicity_d=3),
        MealElement(id="TEST_ELEMENT_3", name="Roast parrot",
                    category="main_course", prep_time_m=10, cooking_time_m=20,  periodicity_d=10),
        MealElement(id="TEST_ELEMENT_4", name="Flamingo boiled with dates",
                    category="main_course", prep_time_m=10, cooking_time_m=20, periodicity_d=3),
    ]
    roman_banquet_meals = {
        # names from https://delishably.com/world-cuisine/ancient-food-rome
        "TEST_FOOD_1": Meal(id="TEST_FOOD_1", name="Boiled ostrich with sweet sauce", periodicity_d=3),
        "TEST_FOOD_2": Meal(id="TEST_FOOD_2", name="Turtledove boiled in its feathers", periodicity_d=5),
        "TEST_FOOD_3": Meal(id="TEST_FOOD_3", name="Pitted dates stuffed with nuts and pine kernels, fried in honey", periodicity_d=1),
        "COMPOUNDED_1": Meal(id="COMPOUNDED_1", name="Ancient Rome Menu", elements="appetiser;main_course")
    }
    history = {
        date(68, 6, 3): ["TEST_ELEMENT_1+TEST_ELEMENT_4", "TEST_FOOD_2"],
        date(68, 6, 4): ["TEST_FOOD_3"],
    }
    planner = MealPlanner(date_from=date(68, 6, 5), elements=roman_banquet_elements, meals=roman_banquet_meals, history=history)
    assert planner.max_periodicity == 10
    suggestions = [s.id for s in planner.get_eligible_meals(date(68, 6, 5))]
    assert "TEST_ELEMENT_1+TEST_ELEMENT_3" not in suggestions
    assert "TEST_ELEMENT_2+TEST_ELEMENT_3" in suggestions

def test_planner_history_element():
        roman_banquet_elements = [
            # names from https://delishably.com/world-cuisine/ancient-food-rome
            MealElement(id="TEST_ELEMENT_1", name="Jellyfish and eggs",
                        category="appetiser", prep_time_m=10, cooking_time_m=20, periodicity_d=3),
            MealElement(id="TEST_ELEMENT_2", name="Sea urchins with spices, honey, oil, and egg sauce",
                        category="appetiser", prep_time_m=10, cooking_time_m=20,  periodicity_d=3),
            MealElement(id="TEST_ELEMENT_3", name="Roast parrot",
                        category="main_course", prep_time_m=10, cooking_time_m=20,  periodicity_d=10),
        ]
        roman_banquet_meals = {
            "COMPOUNDED_1": Meal(id="COMPOUNDED_1", name="Ancient Rome Menu", elements="appetiser;main_course")
        }
        history = {
            date(68, 6, 3): ["TEST_ELEMENT_1"],
        }
        planner = MealPlanner(date_from=date(68, 6, 4), elements=roman_banquet_elements, meals=roman_banquet_meals,
                              history=history)
        suggestions = [s.id for s in planner.get_eligible_meals(date(68, 6, 4))]
        assert suggestions == ["TEST_ELEMENT_2+TEST_ELEMENT_3"]
