import os
import pandas as pd
import sys
import argparse
import utils

def add_features(workbook, act, features, header_map):
    """
    Add features to activity object
    ":param workbook: current excel doc
    :param act: activity object to be populated with features
    :param features: list of features to be added
    :param header_map: map feature type -> col
    :return: passed in act populated with features
    """

    act_feature_map = act["features"]

    for feature in features:
        try:
            row, col = act["row"], header_map[feature]
            content = workbook.iat[row, col]
            act_feature_map[feature] = content

        except KeyError:
            print(f"header feature {feature} not found in excel doc")

    return act

def fill_nan_values(workbook, row_start):
    """
    Fills nan values in workbook with real values to make parsing easier
    :param workbook: current excel doc
    :param row_start: start of activities
    :return: none
    """
    for col in range(len(workbook.columns)):
        curr_val = workbook.iat[row_start, col]
        for row in range(row_start + 1, len(workbook)):
            curr_cell = workbook.iat[row, col]
            if isinstance(curr_cell, float):
                workbook.iat[row, col] = curr_val
                print(workbook.iat[row, col])
            elif curr_val != curr_cell:
                curr_val = curr_cell

def init_act_obj():
    """
    Creates an empty act object. Redundant but documents parameters expected in act object.
    :return: dict representing act object
    """
    act = {"name": None, "row": 0, "features": {}}
    return act
