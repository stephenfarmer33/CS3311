import mysql.connector
from mysql.connector import errorcode

# how to run:
# 1. run CS33311.sql in mysql workbench
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

def connect():
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

def close_connection(cnx):
    cnx.close()
