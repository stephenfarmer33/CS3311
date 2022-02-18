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
            "(ProjectID, Project, State, Budget_Period, Reporting_Period) "
            "VALUES (%(ProjectID)s, %(Project)s, %(State)s, %(Budget Period)s, %(Reporting Period)s);"),
    'activities': ("INSERT INTO projects "
            "(ID, Activity, Description, Outcome, Output, Timeline, Statistics, Status, Successes, Challenges, CDC_Support_Needed) "
            "VALUES (%(ID)s, %(Activity)s, %(Description)s, %(Outcome)s, %(Output)s, %(Timeline)s, %(Statistics)s, %(Status)s, %(Successes)s, %(Challenges)s, %(CDC_Support_Needed)s);")
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

    print('Database connection:', cnx)
    cursor = cnx.cursor()
    

def insert(table, data):
    if table in insert_query:
        try:
            cursor.execute(insert_query[table], data)
            cnx.commit()
        except mysql.connector.Error as err:
            print("Insert failed: {}".format(err))
    else:
        print('Invalid table selected for insertion')

def remove(table, data):
    pass

def close_connection():
    if cnx:
        print('Closed connection:', cnx)
        cnx.close()
        cursor.close()
    else:
        print('No connection to close')

connect()
