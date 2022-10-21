import os

from flask import render_template, redirect, url_for, flash, current_app
from flask_login import login_required
from sqlalchemy.exc import IntegrityError
from werkzeug.datastructures import FileStorage
from werkzeug.utils import secure_filename

from . import meals
from .forms import DishesUploadForm
from .meal_dao import get_all_meals, XlsxDishReader
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
                current_app.config['UPLOAD_PATH'],
                filename
            )
            f.save(fpath)
            new_dishes = XlsxDishReader(fpath).get()
            try:
                db.session.add_all(new_dishes)
                db.session.commit()
                flash(f"Found {len(new_dishes)} dishes in {filename}")
            except IntegrityError as e:
                db.session.rollback()
                flash("Problem found while adding dishes to DB")
                flash(str(e))

            # os.remove(filename)
    else:
        print(upload_form.errors, upload_form.xlsx_file.data.filename)
        flash(upload_form.errors['xlsx_file'][0])
    return redirect(url_for('.list_meals'))
