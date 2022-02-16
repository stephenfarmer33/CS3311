import mysql.connector
from mysql.connector import errorcode

# how to run:
# 1. run CS3311.sql in mysql workbench
# 2. create a custom user with the credentials:
#   user: 'cs3311_admin'
#   password: 'password'
#   administrative roles: DBA
#   schema privileges: add entry -> schema 'CS 3311', Select "ALL" privileges

# database connection config info
config = {
    'user': 'cs3311_admin',
    'password': 'password',
    'host': '127.0.0.1',
    'database': 'CS3311'
}


class sql_connection:
    def __init__(self):
        self.config = {
            'user': 'cs3311_admin',
            'password': 'password',
            'host': '127.0.0.1',
            'database': 'CS3311'
        }
        self.cnx = None
        self.cursor = None

    def connect(self):
        try:
            self.cnx = mysql.connector.connect(**self.config)
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("Something is wrong with your user name or password")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print("Database does not exist")
            else:
                print(err)

        print('Database connection:', self.cnx)
        self.cursor = self.cnx.cursor()
        

    def insert(self, table, data):
        if table == 'projects':
            query = ("INSERT INTO projects "
               "(ProjectID, Project, State, Budget_Period, Reporting_Period) "
               "VALUES (%(ProjectID)s, %(Project)s, %(State)s, %(Budget Period)s, %(Reporting Period)s);")
        elif table == 'activities':
            pass
        if query:
            self.cursor.execute(query, data)
            self.cnx.commit()
            print('Insert executed on table:', table, '\nData:', data)
        else:
            print('Invalid table selected for insertion')


    def close_connection(self):
        if self.cnx:
            print('Closed connection:', self.cnx)
            self.cnx.close()
            self.cursor.close()
        else:
            print('No connection to close')


# example usage
sql = sql_connection()
sql.connect()

table = 'projects'
data = {
    'ProjectID': 101,
    'Project': 'project name',
    'State': 'Georgia',
    'Budget Period': 'budget period dates',
    'Reporting Period': 'reporting period dates'
}
sql.insert(table, data)

sql.close_connection()
