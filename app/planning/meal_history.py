
# dictionary of the following structure:
#   key -> tuple(year,month) ; month indexed from 1 to 12 (0 should not be used)
#   value -> fixed-size list (size=nb day of the month + 1 ; indexed starting from 1) of lists (containing the meals of that day)
import calendar


class MonthDict(dict):
    def __missing__(self, key):
        (year, month) = key
        v = [[] for _ in range(calendar.monthrange(year, month)[1]+1)]
        self[key] = v
        return v

history = MonthDict()

def get_history(year, month):
    return history[(year,month)]

def set_history(year, month, day, meals):
    l = history[(year,month)]
    l[day] = meals
    print("set_history: ", l)

