import os
import re

from flask import render_template, redirect, url_for, flash, current_app, jsonify
from flask_login import login_required
from sqlalchemy.exc import IntegrityError
from werkzeug.datastructures import FileStorage
from werkzeug.utils import secure_filename

from . import meals
from .forms import DishesUploadForm, DishForm
from .dao import get_all_meals, MealsDBAccess
from .dao_xlsx_readers import XlsxReader
from .models import Dish
from .. import db


@meals.route("/meals")
def list_meals():
    upload_form = DishesUploadForm()
    return render_template("meals.html", meals=get_all_meals().values(), upload_form=upload_form)

@meals.route("/meals/upload", methods=["POST"])
@login_required
def upload_meals():
    upload_form = DishesUploadForm()
    if upload_form.validate_on_submit():
        f: FileStorage = upload_form.xlsx_file.data
        filename = secure_filename(f.filename)
        if filename:
            fpath = os.path.join(
                current_app.root_path,
                filename
            )
            f.save(fpath)
            xlsx_reader = XlsxReader(fpath)
            dishes_added = MealsDBAccess.add_all_dishes(db, xlsx_reader.get_dishes())
            ingredients_added = MealsDBAccess.add_all_ingredients(db, xlsx_reader.get_ingredients())
            if dishes_added:
                flash(f"Added {dishes_added} dishes from {filename}")
            if ingredients_added:
                flash(f"Added {ingredients_added} ingredients from {filename}")
            if dishes_added+ingredients_added == 0:
                flash(f"Could not add anything from {filename}")
            os.remove(fpath)
    else:
        print(upload_form.errors, upload_form.xlsx_file.data.filename)
        flash(upload_form.errors['xlsx_file'][0])
    return redirect(url_for('.list_meals'))


@meals.route("/meals/add/<dish_type>", methods=["GET", "POST"])
def add_dish(dish_type: str):
    nav_elts = {
        "dish": "Dish",
        "composed_meal": "Composed meal"
    }
    dish_form = DishForm()
    if dish_form.is_submitted():
        dish_name: str = dish_form.name.data.strip()
        dish_id: str = re.sub("[^A-Z0-9]", "_", dish_name.upper())
        if dish_type == "dish":
            category = dish_form.moment.data
            if category == "-" and dish_form.category_select2.data:
                category = dish_form.category_select2.data
            dish = Dish(
                id=dish_id,
                name=dish_name,
                category=category,
                prep_time_m=dish_form.prep_time.data,
                cooking_time_m=dish_form.cooking_time.data,
                periodicity_d=dish_form.periodicity.data,
            )
        elif dish_type == "composed_meal":
            print(dish_form.elements_select2.data)
            dish = Dish(
                id=dish_id,
                name=dish_name,
                category=dish_form.moment.data,
                prep_time_m=0,
                cooking_time_m=0,
                periodicity_d=0,
                elements=";".join(dish_form.elements_select2.data)
            )
        else:
            raise Exception("Unexpected dish_type")
        try:
            db.session.add(dish)
            db.session.commit()
            flash(f"{dish.name} added")
            return redirect(url_for(".list_meals"))
        except IntegrityError as e:
            db.session.rollback()
    return render_template("add_dish.html", nav_elts=nav_elts, dish_type=dish_type, dish_form=dish_form)

@meals.route("/js/add-dish-script/<dish_type>")
def add_dish_script(dish_type: str):
    return render_template("add-dish-script.js", dish_type=dish_type)

@meals.route("/meals/categories")
def dish_categories():
    categories = [c[0] for c in db.session.query(Dish.category).distinct().all()]
    # TODO: find a way out of this multiple semantic in the category field, it's ugly
    cat_not_moment = [c for c in categories if c not in ["Lunch", "Dinner", "Both"]]
    cat_not_moment.append("")
    return jsonify({"results":
            [{"id": c, "text": c} for c in cat_not_moment]})


