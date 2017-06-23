
params_levels = {
    1: [50, 74, 124, 349, 499], # Dioxid de sulf
    4: [10, 20, 30, 40, 100], # PM 10 aut
    5: [10, 20, 30, 40, 100], # PM 10 grv
    9: [40, 80, 120, 180, 240], # Ozon
    1001: [50, 100, 140, 200, 400], # Dioxid de azot
    19: [10, 20, 35, 40], # Viteza vant
    22: [745, 760, 770, 775], # Presiune

    24: { # Precipitatii
         0: [32.5, 37.5, 42.5, 47.5],
         1: [30, 35, 40, 45],
         2: [28.5, 33.5, 38.5, 43.5],
         3: [40, 45, 50, 55],
         4: [55, 60, 65, 70],
         5: [75, 80, 85, 90],
         6: [50, 55, 60, 65],
         7: [45, 50, 55, 60],
         8: [35, 40, 45, 50],
         9: [42.5, 47.5, 52.5, 57.5],
         10: [40, 45, 50, 55],
         11: [42.5, 47.5, 52.5, 57.5],
    },
    20: { # Temperature
        0: [-5, -3, -1, 1.5],
        1: [-3, -1, 1, 3],
        2: [0, 3, 6, 10],
        3: [5, 9, 12, 15],
        4: [12, 15, 17, 20],
        5: [15, 17, 20, 23],
        6: [15, 19, 23, 26],
        7: [15, 19, 22, 26],
        8: [11, 14, 17, 20],
        9: [6, 9, 12, 15],
        10: [0, 3, 6, 9],
        11: [-4, -1, 2, 5],
    }
}
_MONTHLY_VALUES_PARAMS = [24, 20]



def compute_disease_class(disease_boundaries, disease_value):
    disease_class = 0
    for value in disease_boundaries:
        if disease_value < value:
            break
        else:
            disease_class += 1
    return disease_class


def compute_input_class(parameter_index, parameter_value, month='0'):
    param_class = 0
    values = None

    if parameter_index not in _MONTHLY_VALUES_PARAMS:
        values = params_levels[parameter_index]
    else:
        values = params_levels[parameter_index][month]

    for value in values:
        if parameter_value < value:
            break
        else:
            param_class += 1

    return param_class
