import mysql.connector
from mysql.connector import errorcode

# how to run:
# 1. run CS3311.sql in mysql workbench
#
# 2. create a custom user with the credentials:
#    user: 'cs3311_admin'
#    password: 'password'
#    administrative roles: DBA
#    schema privileges: add entry -> schema 'CS 3311', Select "ALL" privileges
#
# 3. import and run sql_connection in another file.
#    example code found at sql_test.py

config = {
    'user': 'cs3311_admin',
    'password': 'password',
    'host': '127.0.0.1',
    'database': 'CS3311'
}
cnx = None
cursor = None

insert_query = {
    'projects': ("INSERT INTO projects "
            "(Project, State, Budget_Period_Start, Budget_Period_End, Reporting_Period, File_Name) "
            "VALUES (%(Project)s, %(State)s, %(Budget_Period_Start)s, %(Budget_Period_End)s, %(Reporting_Period)s, %(File_Name)s);"),
    'activities': ("INSERT INTO activities "
            "(ProjectID, Activity, Description, Outcome, Output, Timeline, Statistics, Status, Successes, Challenges, CDC_Support_Needed, Parent_File) "
            "VALUES (%(ProjectID)s, %(Activity)s, %(Description)s, %(Outcome)s, %(Output)s, %(Timeline)s, %(Statistics)s, %(Status)s, %(Successes)s, %(Challenges)s, %(CDC_Support_Needed)s, %(Parent_File)s);")
}

select_query = {
    'file_names': "select distinct File_Name from projects;",
}

def connect():
    global cnx
    global cursor
    try:
        cnx = mysql.connector.connect(**config)
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)

    print('Database connection opened:', cnx)
    cursor = cnx.cursor()
    return cursor, cnx
    #return cnx, cursor
    
# insert multiple rows?
def insert(table, data):
    """
    Insert data into table in database
    :param table: str table to insert
    :param data: list of dict of data to insert 
    """
    # can use either single dict or list of dict
    # if type(data) == dict:
    #     data = [data]
    if table in insert_query:
        try:
            cursor.executemany(insert_query[table], data)
            cnx.commit()
        except mysql.connector.Error as err:
            print("Insert failed: {}".format(err))
    else:
        print('Invalid table selected for insertion')

def select(query, data=None):
    if query in select_query:
        res = []
        cursor.execute(select_query[query])
        for d in cursor:
            res.append(d[0])
        return res
    else:
        print('Invalid query')
    
def delete_duplicates(file_name):
    project_ids = []
    print(file_name)
    cursor.execute(f"SELECT ProjectID FROM projects WHERE File_Name = \'{file_name}\';")
    for d in cursor:
        project_ids.append(d[0])
    print('project ids:', project_ids)
    for id in project_ids:
        cursor.execute(f"DELETE FROM activities WHERE ProjectID = \'{id}\'")
        cursor.execute(f"DELETE FROM projects WHERE ProjectID = \'{id}\'")

def close_connection():
    """
    closes SQL connection
    """
    if cnx:
        print('Database connection closed:', cnx)
        cnx.close()
        cursor.close()
    else:
        print('No connection to close')

def get_latest_projectID():
    """
    gets latest projectID for indexing
    """
    cursor.execute('SELECT MAX(ProjectID) from projects;')
    return cursor.fetchone()[0]

#connect()
