import numpy as np
from flask import render_template, redirect, url_for, flash
import os

from . import meals

from .models import Meal, MealType

def read_mock_meals(path):
    print(f"Using mock food data from {path}")
    meals = []
    import pandas as pd
    import numpy as np
    from math import isnan
    food_df = pd.read_excel(path, sheet_name="Food").replace({np.nan:None})
    for idx, row in food_df.iterrows():
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
    Meal(id=1, name="Courgettes", prep_time_m=20, cooking_time_m=25, meal_type=MealType.dinner, periodicity_d=8),
]


@meals.route("/meals")
def meals():
    return render_template("meals.html", meals=mock_meals)
