from flask import Blueprint

planning = Blueprint("planning", __name__)

from . import views