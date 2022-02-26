import os
import pandas as pd
import sys
import argparse

from constants import states
from constants import us_state_to_abbrev


def validate_file_name(file_name):
    file_name = os.path.basename(file_name)
    state = file_name.split(" ")[0]
    if len(state) == 1:
        state = file_name.split("_")[0]

    if state not in states or state not in us_state_to_abbrev:
        print("expected file name to be formatted as {State} {EH####} {Year #} {File Name}")
        return False
    return True


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
            act_feature_map[feature] = None

    return act


def fill_nan_values(workbook, row_start, features):
    """
    Fills nan values in workbook with real values to make parsing easier
    :param workbook: current excel doc
    :param row_start: start of activities
    :param features: features to fill
    :return: none
    """
    for col in range(len(workbook.columns)):
        curr_val = workbook.iat[row_start, col]
        if curr_val in features:
            for row in range(row_start + 1, len(workbook)):
                curr_cell = workbook.iat[row, col]
                if isinstance(curr_cell, float):
                    workbook.iat[row, col] = curr_val
                elif curr_val != curr_cell:
                    curr_val = curr_cell


def get_state_and_plans(file_name, workbook):
    """
    :param file_name: name of file being parsed
    :param workbook: dataframe of excel file parsed
    :return: tuple containing state, year
    """
    file_name = os.path.basename(file_name)
    print(file_name)
    state = file_name.split(" ")[0]
    if len(state) == 1:
        state = file_name.split("_")[0]

    # convert full state name into abbrev
    if state in us_state_to_abbrev:
        state = us_state_to_abbrev[state]

    row, col = find_entry(workbook, "Budget Period")
    # year is non constant cols to the right of budget period
    year = None
    while isinstance(year, float) or year is None:
        col += 1
        year = workbook.iat[row, col]

    print(f"state: {state}")
    print(f"year: {year}")
    return state, year


def find_entry(workbook, string):
    """
    :param workbook: dataframe of excel file being parsed
    :param string: string to search for
    :return: row, col of first cell with string inside
    """
    header_row, num_rows, num_cols = 0, len(workbook), len(workbook.columns)
    for row in range(0, num_rows):
        for col in range(0, num_cols):
            if string in workbook.iat[row, col]:
                print(workbook.iat[row, col])
                return row, col

    return None


def init_act_obj():
    """
    Creates an empty act object. Redundant but documents parameters expected in act object.
    :return: dict representing act object
    """
    act = {}
    act["name"] = None  # name of activity
    act["row"] = None  # row which to find activity in excel sheet
    act["features"] = {}  # map of features
    act["state"] = None  # state of activity (GA, CA, etc)
    act["year"] = None  # budget period of current activities (August 1, 2019 - July 31, 2020, etc)
    return act
