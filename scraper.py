import os
import pandas as pd
import sys
import argparse
import utils

# need xlrd version xlrd==1.2.0

def command_line_parsing():
    """
    :return: Folder path, either given by user or default folder path
    """
    parser = argparse.ArgumentParser(description='Process Public Health Information for Database Dumping',
                                     prog='Database Dump')
    parser.add_argument('-f', '--folder',
                        help='Location of the folder containing the files to be processed. If using the default (dummy) folder, do not use this option')

    args = parser.parse_args()
    folder = args.folder

    if sys.platform == 'darwin':
        slash = '/'
    else:
        slash = '\\'

    if folder is None:
        folder = os.path.dirname(os.path.abspath(__file__)) + slash + "dummy"
    elif not os.path.isdir(folder):
        print('The folder specified does not exist')
        sys.exit()
    return folder


def valid_extension(file_name):
    """
    :param file_name: name of the file
    :return: True if file has a valid extenstion, false otherwise
    """
    valid_ext = {'pdf', 'xlsx', 'docx', 'doc', 'xls'}
    ext = file_name.split(".")
    return len(ext) == 2 and ext[1] in valid_ext


def parse_activities(file_name, file_type):
    """
    :param file_name: file being parsed
    :param file_type: file type being parsed
    :return: dictionary of activities
    """
    acts = {}
    if file_type in {"xlsx", "xls"}:
        # Open the Workbook
        try:
            workbook = pd.read_excel(file_name, sheet_name="Work Plan", header=4)
        except ValueError:
            return False

        # Find header row start
        header_row, num_rows, num_cols = 0, len(workbook), len(workbook.columns)
        for row in range(0, num_rows):
            for col in range(0, num_cols):
                if workbook.iat[row, col] == "Project Title":
                    header_row = row
                    break

        print(f"header row is {header_row}")
        # map activity feature
        header_map = {}
        headers = ["Project Title", "Activity Title", "Activity", "Activity Description", "Timeline", "Status",
                   "Successes", "Challenges", "CDC Program Support Needed"]

        # features each excel doc is expected to have
        core_features = ["Activity Title", "Activity", "Activity Description", "Timeline"]


        for col in range(0, num_cols):
            curr_header = workbook.iat[header_row, col]
            if curr_header in headers:
                header_map[curr_header] = col

        print(f"header map is {header_map}")

        # map_acts_to_project(workbook, header_map, header_row)

        # find all activities
        act_col = header_map["Activity Title"]
        for row in range(header_row + 1, num_rows):
            curr_act = utils.init_act_obj()
            curr_act_name = workbook.iat[row, act_col]
            curr_act["name"] = curr_act_name
            curr_act["row"] = row

            utils.add_features(workbook, curr_act, core_features, header_map)
            print(curr_act)
            acts[curr_act_name] = curr_act


def map_acts_to_project(workbook, header_map, header_row):
    """
    :param workbook: current excel document being read
    :param header_map: dict mapping header names -> col indexes
    :param: header_row: row index of headers
    :return: dict projects mapping project name to list of activities associated with project
    """

    projects = {}
    curr_acts = []
    curr_project = None
    for row in range(header_row + 1, len(workbook)):
        curr_cell = workbook.iat[row, header_map["Project Title"]]
        print(f"curr cell: {curr_cell} and type is {type(curr_cell)}")
        if not isinstance(curr_cell, float) and curr_project != curr_cell:
            print(f"new project {curr_cell} detected")
            # new project starts in this row, fill last project's activities
            if curr_project is not None:
                projects[curr_project] = curr_acts[:]
                print(f"activities {curr_acts} appended to project: {curr_project}")
                print(f"project {curr_project} added to projects!")
            curr_project = curr_cell
            curr_acts = []

        act = workbook.iat[row, header_map["Activity Title"]]
        curr_acts.append(act)

    # add last project
    if curr_project not in projects:
        projects[curr_project] = curr_acts[:]
        print(f"activities {curr_acts} appended to project: {curr_project}")
        print(f"project {curr_project} added to projects!")

    for project in projects.keys():
        print(f"{project} : {projects[project]}")

    return projects


def valid_content(file_name, file_type):
    """
    :param file_name: file being parsed
    :param file_type: file type being parsed
    :return: True if contents of file are valid, False otherwise
    """

    if file_type in {"xlsx", "xls"}:
        # Open the Workbook
        try:
            workbook = pd.read_excel(file_name, sheet_name="Work Plan", header=4)
        except ValueError:
            return False

        # Valid Columns for the Data
        valid_columns = ["Project Title", "Activity Title", "Strategy", "Activity", "Activity Description", "Output",
                         "Short-Term Outcome", "Timeline", "Status", "Successes", "Challenges",
                         "CDC Program Support Needed"]
        # Iterate through Excel sheet and check if given data matches correct data
        for i in range(0, 12):
            try:
                print(workbook.iat[0, i])

            except IndexError:
                return False

    elif file_type in {"pdf"}:
        # ToDO
        hello = 1 + 1

    elif file_type in {"doc", "docx"}:
        # ToDo
        hello = 1 + 1

    return True


def parse(file_name, file_type):
    # Finds specific sheet in excel and prints as dataframe
    desired_sheet = 'Work Plan'
    if file_type in {"xlsx"}:
        # Open the Workbook
        xl = pd.ExcelFile(file_name)
        # Chosse a specific sheet
        if desired_sheet in xl.sheet_names:
            workbook = pd.read_excel(file_name, sheet_name=desired_sheet)
            # print(workbook)


def classify_files(path):
    """
    :param path: path of the directory with target files
    :return: dictionary containing classification of files into 3 categories: valid, invalid_ext, invalid_cont
    """
    valid, invalid_ext, invalid_cont = "valid", "invalid_ext", "invalid_cont"

    categories = {
        valid: [],
        invalid_ext: [],
        invalid_cont: []
    }

    # get all files in path directory
    # os.chdir(path)
    file_names = next(os.walk(path))[2]
    print(f"files in directory: {file_names}")

    # classify and parse all files in path directory
    for file_name in file_names:
        # classification
        file_type = file_name.split(".")[1]

        parse_activities(os.path.join(path, file_name), file_type)

        # if not valid_extension(file_name):
        #     categories[invalid_ext].append(file_name)
        #
        # elif not valid_content(os.path.join(path, file_name), file_type):
        #     categories[invalid_cont].append(file_name)
        #
        # else:
        #     categories[valid].append(file_name)

        # parsing
        # parse(os.path.join(path, file_name), file_type)

    print('------------')

    print(f"Valid: {categories[valid]}")
    print(f"Invalid Extension: {categories[invalid_ext]}")
    print(f"Invalid Content: {categories[invalid_cont]}")

    return categories


# New CMD Line argument main method
# python3 scraper.py dummy
def main():
    folder = command_line_parsing()
    classify_files(folder)


if __name__ == "__main__":
    main()
