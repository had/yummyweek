from flask import Blueprint

meals = Blueprint("meals", __name__)

from .models import Meal, MealType
import os

def read_mock_meals(path):
    print(f"Using mock food data from {path}")
    meals = []
    import pandas as pd
    import numpy as np
    from math import isnan
    food_df = pd.read_excel(path, sheet_name="Food").replace({np.nan:None})
    for _, row in food_df.iterrows():
        d = row.to_dict()
        mtype = d['meal_type']
        period = d['periodicity_d']
        if mtype == MealType.batch_cooking or (period is float and isnan(period)):
            # skip
            continue
        meals.append(Meal(**d))
    print(f"Found {len(meals)} meals")
    return meals

mock_food_env = os.environ.get('MOCK_FOOD')
mock_meals = read_mock_meals(mock_food_env) if mock_food_env else [
    Meal(id="COURGETTES", name="Courgettes", prep_time_m=20, cooking_time_m=25, meal_type=MealType.dinner, periodicity_d=8),
]

from . import views

