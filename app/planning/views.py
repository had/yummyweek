from flask import render_template, redirect, url_for, flash

from . import planning
from datetime import datetime
from calendar import Calendar

weekdays = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
monthnames = ['January', 'Febuary', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November',
          'December']

@planning.route("/plans")
def plans():
    now = datetime.now()
    cal = Calendar()
    return render_template("plans.html", monthyear = (monthnames[now.month-1], now.year), weekdays = weekdays,
                           weeks = cal.monthdayscalendar(now.year, now.month))
