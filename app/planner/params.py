import os


def read_params_xls(path):
    print(f"Using params data from {path}")
    import pandas as pd
    import numpy as np
    params = {}
    params_df = pd.read_excel(path, sheet_name="planner_parameters").replace({np.nan: None})
    for _, row in params_df.iterrows():
        d = row.to_dict()
        day = d['day']
        del d['day']
        params[day] = d
    return params


xls_params_env = os.environ.get('YUMMYWEEK_XLS')
xls_params = read_params_xls(xls_params_env) if xls_params_env else {}


def get_params():
    return xls_params
