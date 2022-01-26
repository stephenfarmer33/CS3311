import os
# import xlrd
import pandas as pd
import sys
import argparse

# need xlrd version xlrd==1.2.0

def command_line_parsing():
    """
    :return: Folder path, either given by user or default folder path
    """
    parser = argparse.ArgumentParser(description='Process Public Health Information for Database Dumping', prog='Database Dump')
    parser.add_argument('-f', '--folder', help='Location of the folder containing the files to be processed. If using the default (dummy) folder, do not use this option')

    args = parser.parse_args()
    folder = args.folder
    if folder is None:
        folder = os.path.dirname(os.path.abspath(__file__)) + "\\dummy"
    elif not os.path.isdir(folder):
        print('The folder specified does not exist')
        sys.exit()
    return folder

def valid_extension(file_name):
    """
    :param file_name: name of the file
    :return: True if file has a valid extenstion, false otherwise
    """
    valid_ext = {'pdf', 'xlsx', 'docx', 'doc', 'csv', 'xls'}
    ext = file_name.split(".")
    return len(ext) == 2 and ext[1] in valid_ext


def valid_content(file_name, file_type):
    """
    :param file_name: file being parsed
    :param file_type: file type being parsed
    :return: True if contents of file are valid, False otherwise
    """

    if file_type in {"xlsx", "xls", 'csv'}:
        # Open the Workbook
        workbook = pd.read_excel(file_name, header=4)

        # Valid Columns for the Data
        valid_columns = ["Project Title", "Activity Title", "Strategy", "Activity", "Activity Description", "Output",
                         "Short-Term Outcome", "Timeline", "Status", "Successes", "Challenges",
                         "CDC Program Support Needed"]
        # Iterate through Excel sheet and check if given data matches correct data
        for i in range(0, 12):
            try:
                if not (workbook.iat[0, i] in valid_columns):
                    return False
            except IndexError:
                return False

    elif file_type in {"pdf"}:
        #ToDO
        hello = 1+1
    
    elif file_type in {"doc", "docx"}:
        #ToDo
        hello = 1+1
    
    return True

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
    os.chdir(path)
    # mac compatibility
    if sys.platform == 'darwin':
        slash = '/'
    else:
        slash = '\\'
    os.chdir(os.getcwd() + slash + path)
    file_names = next(os.walk('.'))[2]
    print(f"files in directory: {file_names}")

    # classify all files in path directory
    for file_name in file_names:
        if not valid_extension(file_name):
            categories[invalid_ext].append(file_name)

        elif not valid_content(file_name, file_name.split(".")[1]):
            categories[invalid_cont].append(file_name)

        else:
            categories[valid].append(file_name)

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
