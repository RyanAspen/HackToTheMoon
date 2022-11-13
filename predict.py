import math
from joblib import load
from sklearn.linear_model import LinearRegression
from sklearn import preprocessing
from sklearn.preprocessing import PolynomialFeatures

powers = [3, 2, 3, 2]

bit_names = ["Buzz Drilldrin", "AstroBit", "Apollo", "ChallengDriller"]


def predict(X, bit_name):
    bit_name_id = bit_names.index(bit_name)
    model_file_name = f"model{bit_name_id + 1}.joblib"
    clf = load(model_file_name)
    X = preprocessing.scale(X)
    poly = PolynomialFeatures(degree=powers[bit_name_id], include_bias=False)
    poly_X = poly.fit_transform(X)
    return clf.predict(poly_X)


import pandas as pd
d={"HOOK_LOAD":43.0, "DIFFERENTIAL_PRESSURE":343.0, "WEIGHT_ON_BIT":3434.0, "DRILL_BIT_NAME":"AstroBit"}
ser = pd.Series(data=d)
def get_derivative(row):
    bit_name = row["DRILL_BIT_NAME"]
    bit_name_id = bit_names.index(bit_name)
    model_file_name = f"model{bit_name_id + 1}.joblib"
    clf = load(model_file_name)

    # Get derivatives of model function
    coeficients = clf.coef_
    der_h = 0
    der_d = 0
    der_w = 0
    for p in range(powers[bit_name_id] + 1):
        i = 0
        for x in range(int(math.pow(3, p))):
            skip = False
            bx = bin(x)[-3:]
            for i2 in range(1, len(bx)):
                if bx[i2] < bx[i2 - 1]:
                    skip = True
                    break
            if skip:
                continue
            h_power = bx.count("0")
            d_power = bx.count("1")
            w_power = bx.count("2")
            if h_power > 0:
                der_h += coeficients[i] * (row["HOOK_LOAD"] ** (h_power - 1)) \
                         * (row["DIFFERENTIAL_PRESSURE"] ** d_power) * (row["WEIGHT_ON_BIT"] ** w_power)
            if d_power > 0:
                der_d += coeficients[i] * row["DIFFERENTIAL_PRESSURE"] ** (d_power - 1) \
                         * (row["HOOK_LOAD"] ** h_power) * (row["WEIGHT_ON_BIT"] ** w_power)
            if w_power > 0:
                der_w += coeficients[i] * row["WEIGHT_ON_BIT"] ** (w_power - 1) \
                         * (row["DIFFERENTIAL_PRESSURE"] ** d_power) * (row["HOOK_LOAD"] ** h_power)
            i += 1

    return der_h, der_d, der_w


def advise(row):
    # Get derivatives of model function
    der_h, der_d, der_w = get_derivative(row)

    advice = []

    if der_h < 0:
        # HOOK_LOAD is causing things to get worse, try increasing and decreasing
        temp_row_less = row
        temp_row_less[0] -= 0.1
        der_h, _, _ = get_derivative(row)
        if der_h > 0:
            advice.append("Decrease HOOK_LOAD")
        else:
            temp_row_more = row
            temp_row_more[0] += 0.1
            der_h, _, _ = get_derivative(temp_row_more)
            if der_h > 0:
                advice.append("Increase HOOK_LOAD")
            else:
                return ["Replace bit"]

    if der_d < 0:
        # DIFFERENTIAL_PRESSURE is causing things to get worse, try increasing and decreasing
        temp_row_less = row
        temp_row_less[1] -= 0.1
        _, der_d, _ = get_derivative(temp_row_less)
        if der_d > 0:
            advice.append("Decrease DIFFERENTIAL_PRESSURE")
        else:
            temp_row_more = row
            temp_row_more[1] += 0.1
            _, der_d, _ = get_derivative(temp_row_more)
            if der_h > 0:
                advice.append("Increase DIFFERENTIAL_PRESSURE")
            else:
                return ["Replace bit"]

    if der_w < 0:
        # WEIGHT_ON_BIT is causing things to get worse, try increasing and decreasing
        temp_row_less = row
        temp_row_less[2] -= 0.1
        _, _, der_w = get_derivative(temp_row_less)
        if der_w > 0:
            advice.append("Decrease WEIGHT_ON_BIT")
        else:
            temp_row_more = row
            temp_row_more[2] += 0.1
            __, _, der_w = get_derivative(temp_row_more)
            if der_w > 0:
                advice.append("Increase WEIGHT_ON_BIT")
            else:
                return ["Replace bit"]
    return advice
