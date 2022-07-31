from flask import Blueprint

meals = Blueprint("meals", __name__)

from . import views

