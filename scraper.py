import os
import pandas as pd
import sys
import argparse
import utils
from tkinter import *
from tkinter.ttk import *
# from tkinter.filedialog import askopenfile
from tkinter import filedialog
import time
import threading
import sql_connection

# need xlrd version xlrd==1.2.0

def main_screen():
    data = Tk()
    data.title('Data Extraction')
    data.geometry('400x200')
    # data.state('zoomed')
    return data

def extract_file(success, error, path_box):
    path_box.delete(0, END)
    success.grid_remove()
    error.grid_remove()
    file_path = filedialog.askopenfile(mode='r', filetypes=[('All Files', '*.*'), ('Pdf file', '*.pdf'), ('Excel File', '*.xlsx'), ('Word File', '*.docx'), ('Word File', '*.doc'), ('Excel File', '*.xls'), ('Excel File', '*.xlsb')])
    if file_path is not None:
        path_box.insert(0, file_path.name)
        #file.set(file_path.name)

def extract_folder(success, error, path_box):
    path_box.delete(0, END)
    success.grid_remove()
    error.grid_remove()
    folder_path = filedialog.askdirectory()
    if folder_path is not None:
        path_box.insert(0, folder_path)
        #folder.set(folder_path)

def upload(data, error, success, path_box):
    #file_path = file.get()
    #folder_path = folder.get()
    if(path_box.get() == ""):
        error.grid()
        return
    #if(folder_path == "" and file_path == ""):
    #    error.grid()
    #    return

    progress_bar = Progressbar(data,
                                orient=HORIZONTAL,
                                length=100,
                                mode='indeterminate')
    progress_bar.grid(row=5, columnspan=3, pady=20)
    progress_bar.start()

    # progress_bar_finished = Progressbar(data,
    #                             orient=HORIZONTAL,
    #                             length=100,
    #                             mode='determinate')
    # progress_bar_finished['value'] = 100

    path_thread = threading.Thread(target=classify_files, args=(path_box.get(),))
    path_thread.start()
    while(path_thread.is_alive()):
        data.update()
        pass
    progress_bar.destroy()
    #progress_bar_finished.grid(row=5, columnspan=3, pady=20)
    #progress_bar_finished.grid(row=5, columnspan=3, pady=20)
    # if(folder_path != ""):
    #     folder_thread = threading.Thread(target=classify_files, args=(folder_path,))
    #     folder_thread.start()
    #     print("Passing Folder")

    # else:
    #     file_thread = threading.Thread(target=classify_files, args=(file_path,))
    #     print(file_path)
    #     file_thread.start()
    #     print("Passing File")

    # for i in range(5):
    #     data.update_idletasks()
    #     progress_bar['value'] += 20
    #     time.sleep(1)
    # progress_bar.destroy()
    #file.set("")
    #folder.set("")
    path_box.delete(0, END)
    success.grid()
    

def GUI(data):
    #file = StringVar()
    #folder = StringVar()
    
    success = Label(data, text="Succesful Upload!", foreground='green')
    success.grid(row=6, columnspan=3, pady=10)
    success.grid_remove()
    
    error = Label(data, text="Error! No File or Folder Chosen!", foreground='red')
    error.grid(row=6, columnspan=3, pady=10)
    error.grid_remove()

    path_box = Entry(data, text="Full Path Here:", width=60)
    path_box.grid(row=3, column=0)

    choose_upload = Label(data,
                         text='Choose One: File or Folder. Please choose folder with files inside.')
    choose_upload.grid(row=0, column=0, padx=20)

    file_upload_button = Button(data,
                                text='Choose File',
                                command=lambda:extract_file(success, error, path_box))
    file_upload_button.grid(row=1, column=0)

    folder_upload_button = Button(data,
                                text='Choose Folder',
                                command=lambda:extract_folder(success, error, path_box))
    folder_upload_button.grid(row=2, column=0)




    upload_button = Button(data,
                            text="Upload",
                            command=lambda:upload(data, error, success, path_box))
    upload_button.grid(row=4, columnspan=2, pady=10)



def command_line_parsing():
    """
    :return: Folder path, either given by user or default folder path
    """
    parser = argparse.ArgumentParser(description='Process Public Health Information for Database Dumping',
                                     prog='Database Dump')
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-f', '--folder', help='Location of the folder containing the files to be processed.')
    group.add_argument('-fi', '--file', help='Singular file to be processed. Please put full (absolute) path of file')
    # parser.add_argument('-f', '--folder', help='Location of the folder containing the files to be processed. If using the default (dummy) folder, do not use this option')
    # parser.add_argument('-fi', '--file', help='Singular file to be processed')

    args = parser.parse_args()
    folder = args.folder
    file = args.file
    
    if sys.platform == 'darwin':
        slash = '/'
    else:
        slash = '\\'

    if folder is None and os.path.isfile(file):
        return file
    elif (os.path.isdir(folder)):
        return folder
    else:
        print("Path specified does not exist")
        sys.exit()


def valid_extension(file_name):
    """
    :param file_name: name of the file
    :return: True if file has a valid extenstion, false otherwise
    """
    valid_ext = {'pdf', 'xlsx', 'docx', 'doc', 'xls', 'xlsb'}
    ext = file_name.split(".")
    return len(ext) == 2 and ext[1] in valid_ext


def parse_activities(file_name, file_type):
    """
    :param file_name: file being parsed
    :param file_type: file type being parsed
    :return: dictionary of activities
    """

    acts = {}
    if file_type.lower() in {"xlsx", "xls", "xlsb"}:
        # Open the Workbook
        try:
            workbooks = get_all_workplans(file_name, file_type)
        except ValueError as v:
            print(v)
            return None

        for workbook in workbooks:
            # get state and year from file_name
            state, year = utils.get_state_and_plans(file_name, workbook)
            # Find header row start
            header_row, num_rows, num_cols = 0, len(workbook), len(workbook.columns)
            for row in range(0, num_rows):
                for col in range(0, num_cols):
                    if workbook.iat[row, col] == "Project Title":
                        header_row = row
                        break

            utils.fill_nan_values(workbook, header_row, ["Project Title"])

            # map activity feature
            header_map = {}
            # todo: add outcomes... to thing
            headers = ["Project Title", "Activity Title", "Activity", "Activity Description", "Timeline", "Status",
                       "Successes", "Challenges", "CDC Program Support Needed"]

            for col in range(0, num_cols):
                curr_header = workbook.iat[header_row, col]
                if curr_header in headers:
                    header_map[curr_header] = col


            act_col = header_map["Activity"]
            for row in range(header_row + 1, num_rows):
                curr_act = utils.init_act_obj()
                curr_act_name = workbook.iat[row, act_col]
                if isinstance(curr_act_name, float):
                    continue
                curr_act["name"] = curr_act_name
                curr_act["row"] = row
                curr_act["state"] = state
                curr_act["year"] = year
                curr_act["file"] = os.path.basename(file_name)
                utils.add_features(workbook, curr_act, headers, header_map)
                # print(curr_act)
                acts[curr_act_name] = curr_act
        return acts

    else:
        print(f"file {file_name} extension {file_type} not supported. Scraper only supports xlsx, xls, xlsb file extensions")
        return None


def get_all_workplans(file_name, file_ext):
    # Finds specific sheet in excel and prints as dataframe
    excel_engine = "pyxlsb" if file_ext in {"xlsb"} else "openpyxl"
    workplans = []
    wk_plan = 'workplan'
    # Open the Workbook
    xl = pd.ExcelFile(file_name, engine=excel_engine)
    # Choose a specific sheet
    for desired_sheet in xl.sheet_names:
        fmt_sheet = desired_sheet.replace(" ", "").lower()
        if wk_plan in fmt_sheet and "dontdelete" not in fmt_sheet:
            workbook = pd.read_excel(file_name, sheet_name=desired_sheet, engine=excel_engine)
            workplans.append(workbook)
    return workplans

def insert_acts_into_db(acts):
    """
    inserts activities and projects into database
    :param acts: dictionary of activities (output of parse_activities())
    :return: bool if success
    """
    # insert projects
    project_title = None
    state = None
    budget_period = None
    reporting_period = None
    added_projects = set()
    # insert activities
    
    for activity, values in acts.items():
        features = values['features']
        project_title = features['Project Title']
        state = values['state']
        budget_period = values['year']

        # todo: parse datetime
        # add projects
        if project_title not in added_projects:
            added_projects.add(project_title)

            data = [{
                'Project': project_title,
                'State': state,
                'Budget_Period_Start': '1998-01-01',
                'Budget_Period_End': '1998-01-01',
                'Reporting_Period': '1998-01-01'
            }]
            sql_connection.insert('projects', data)

        latest_id = sql_connection.get_latest_projectID()
        # headers = ["Project Title", "Activity Title", "Activity", "Activity Description", "Timeline", "Status",
                    #    "Successes", "Challenges", "CDC Program Support Needed"]
        
        activity = features['Activity']
        description = features['Activity Description']
        timeline = features['Timeline']
        status = features['Status']
        successes = features['Successes']
        challenges = features['Challenges']
        CDC_Support_Needed = features['CDC Program Support Needed']

        #print(type(successes), successes)
        data = [{
            'ProjectID': latest_id,
            'Activity': activity,
            'Description': description,
            'Outcome': 'sample outcome',
            'Output' : 'sample output',
            'Timeline': timeline,
            'Statistics': 'sample statistics',
            'Status': status,
            'Successes': successes,
            'Challenges': challenges,
            'CDC_Support_Needed': CDC_Support_Needed,
            'Parent_File' : 'sample parent file'
        }]
        for k in data[0]:
            if str(data[0][k]) == 'nan':
                data[0][k] = None
        sql_connection.insert('activities', data)
    return True

def classify_files(path):
    """
    :param path: path of the directory with target files
    :return: dictionary containing classification of files into 3 categories: valid, invalid_ext, invalid_cont
    """
    success, failed, invalid = "success", "failed", "invalid"

    categories = {
        success: [],
        failed: [],
        invalid: []
    }

    # get all files in path directory
    file_names = next(os.walk(path))[2] if os.path.isdir(path) else [path]
    print(f"files in directory: {file_names}")
    for file_name in file_names:
        try:
            file_type = file_name.split(".")[-1]
            curr_file_acts = parse_activities(os.path.join(path, file_name), file_type)
            categories[invalid].append(os.path.basename(file_name)) if curr_file_acts is None else categories[success].append(os.path.basename(file_name))
            if curr_file_acts is not None:
                print(f"num of acts found: {len(curr_file_acts)}")
            # insert into database
            print("------------------------------------------------")
            insert_acts_into_db(curr_file_acts)

        except Exception as e:
            categories[failed].append(os.path.basename(file_name))
            print(f"{os.path.basename(file_name)} failed to parse")
            print(e)

    print('------------')
    print(f"Valid: {categories[success]}")
    print(f"Invalid Extension: {categories[failed]}")
    print(f"Invalid Content: {categories[invalid]}")

    return categories


# New CMD Line argument main method
# python3 scraper.py -f dummy
def main():
    data = main_screen()
    GUI(data)
    data.mainloop()
    sql_connection.close_connection()
    # folder = command_line_parsing()
    # classify_files(folder)


if __name__ == "__main__":
    main()
