import os

from cachetools.func import ttl_cache

from app.meals.models import Dish, Ingredient

mock_food_env = os.environ.get('YUMMYWEEK_XLS')


class XlsxReader:
    def __init__(self, path=mock_food_env):
        self.path = path

    def to_dishes(self) -> list[Dish]:
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
            try:
                dishes.append(Dish(**d))
            except:
                print("XlsxDishReader Issue with " + d['id'])
        return dishes

    @ttl_cache(maxsize=1, ttl=300)
    def get_dishes(self) -> list[Dish]:
        return self.to_dishes()

    def get_ingredients(self) -> list[Ingredient]:
        import pandas as pd
        import numpy as np
        ingredients = []
        ingredients_df = pd.read_excel(self.path, sheet_name="food_ingredients_categories").replace({np.nan: None})
        for _, row in ingredients_df.iterrows():
            d = row.to_dict()
            ingredients.append(Ingredient(**d))
        return ingredients

