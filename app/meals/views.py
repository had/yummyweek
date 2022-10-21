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
                filename
            )
            f.save(fpath)
            new_dishes = XlsxDishReader(fpath).get()
            from collections import Counter
            print("Duplicates: " + str([d for d, c in Counter([d.id for d in new_dishes]).items() if c > 1]))
            added = 0
            for d in new_dishes:
                print(f"Adding {d.id}")
                try:
                    db.session.add(d)
                    db.session.commit()
                    added += 1
                except IntegrityError as e:
                    db.session.rollback()
            flash(f"Added {added} dishes from {filename}")
            os.remove(fpath)
    else:
        print(upload_form.errors, upload_form.xlsx_file.data.filename)
        flash(upload_form.errors['xlsx_file'][0])
    return redirect(url_for('.list_meals'))
