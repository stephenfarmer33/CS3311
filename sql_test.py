import sql_connection

# specify table to query
table = 'projects'

# specify data you want to query with
data = [{
    'ProjectID': 124, # make sure primary key isn't duplicated!!
    'Project': 'project name',
    'State': 'Georgia',
    'Budget Period': 'budget period dates',
    'Reporting Period': 'reporting period dates'
}]

data_many = [{
    'ProjectID': 120, # make sure primary key isn't duplicated!!
    'Project': 'project name',
    'State': 'Georgia',
    'Budget Period': 'budget period dates',
    'Reporting Period': 'reporting period dates'
}, {
    'ProjectID': 121, # make sure primary key isn't duplicated!!
    'Project': 'project name',
    'State': 'Georgia',
    'Budget Period': 'budget period dates',
    'Reporting Period': 'reporting period dates'
}]

# insert data into db with given table and data
sql_connection.insert(table, data)

# close the connection
sql_connection.close_connection()