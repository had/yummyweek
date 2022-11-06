from .. import db
from enum import Enum


class MealType(Enum):
    lunch = "Lunch"
    dinner = "Dinner"
    both = "Both"
    batch_cooking = "Batch"


class Ingredient(db.Model):
    __tablename__ = "ingredients"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True)
    category = db.Column(db.String)


class DishIngredient(db.Model):
    __tablename__ = "dish_ingredients"
    # id = db.Column(db.Integer, primary_key=True)
    dish_id = db.Column(db.String, db.ForeignKey("dishes.id"), primary_key=True)
    ingredient_id = db.Column(db.Integer, db.ForeignKey("ingredients.id"), primary_key=True)
    quantity = db.Column(db.String)
    unit = db.Column(db.String)
    ingredient = db.relationship("Ingredient")


class Dish(db.Model):
    __tablename__ = "dishes"
    id = db.Column(db.String, primary_key=True)
    name = db.Column(db.String, nullable=False)
    category = db.Column(db.String, nullable=False)
    elements = db.Column(db.String)
    prep_notes = db.Column(db.String)
    prep_time_m = db.Column(db.Integer, default=0, nullable=False)
    cooking_notes = db.Column(db.String)
    cooking_time_m = db.Column(db.Integer, default=0, nullable=False)
    cooking_time_comments = db.Column(db.String)
    periodicity_d = db.Column(db.Integer, default=0, nullable=False)
    tags = db.Column(db.String)
    ingredients = db.relationship("DishIngredient")

    def __repr__(self):
        params = ", ".join([f"{a}={getattr(self, a)}" for a in ["id", "name", "category", "elements", "prep_time_m",
                                                                "cooking_time_m", "periodicity_d"]])
        return f"Dish({params})"

    @staticmethod
    def parse_ingredients(ingredients_str: str) -> list[DishIngredient]:
        dish_ingredients = []
        # ingredients_str is a string list of pipe-separated ingredient names,
        # optionally (after a "*" character) with a quantity and a unit. Example of ingredients:
        # "Potatoes*300 g" => explicitly 300g potatoes
        # "Salt" => implicitly some salt
        # "Lemon*2" => implicitly 2 lemon
        # These 3 grouped together form the string list:
        #   "Potatoes*300 g|Salt|Lemon*2"
        for quantified_ingredient in ingredients_str.split("|"):
            di_dict = {}  # dictionary to build a DishIngredient instance
            if "*" in quantified_ingredient:
                ingredient_str, quantity_units = quantified_ingredient.split("*")
                if " " in quantity_units:
                    di_dict["quantity"], di_dict["unit"] = quantity_units.split(" ")
                else:
                    di_dict["quantity"] = quantity_units
            else:
                ingredient_str = quantified_ingredient
            di = DishIngredient(**di_dict)
            di.ingredient = Ingredient.query.filter_by(name=ingredient_str).one()
            dish_ingredients.append(di)
        return dish_ingredients

    @staticmethod
    def from_row(dish_dict):
        if dish_dict['active'] != 'Y':
            return None
        del dish_dict['active']
        if 'ingredients' in dish_dict:
            ingredients_str = dish_dict['ingredients']
            del dish_dict['ingredients']
            try:
                dish_dict['ingredients'] = Dish.parse_ingredients(ingredients_str)
            except Exception as e:
                pass
        return Dish(**dish_dict)


class MealHistory(db.Model):
    __tablename__ = "meal_history"
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date)
    meal = db.Column(db.String)
