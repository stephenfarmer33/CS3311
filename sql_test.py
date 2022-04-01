import sql_connection
from datetime import date

# specify table to query
table = 'projects'

# specify data you want to query with
data = [{
    'Project': 'project name',
    'State': 'Georgia',
    'Budget_Period_Start': '1998-01-01',
    'Budget_Period_End': '1998-01-01',
    'Reporting_Period': '1998-01-01',
    'File_Name': 'test name'
}]

data_many = [{
    'Project': 'project name',
    'State': 'Georgia',
    'Budget Period': 'budget period dates',
    'Reporting Period': 'reporting period dates'
}, {
    'Project': 'project name',
    'State': 'Georgia',
    'Budget Period': 'budget period dates',
    'Reporting Period': 'reporting period dates'
}]

latest_id = sql_connection.get_latest_projectID()

table_activities = 'activities'

data_activities = [{
    'ProjectID': latest_id,
    'Activity': 'sample activity',
    'Description': 'sample description',
    'Outcome': 'sample outcome',
    'Output' : 'sample output',
    'Timeline': 'sample timeline',
    'Statistics': 'sample statistics',
    'Status': 'sample status',
    'Successes': 'sample successes',
    'Challenges': 'sample challenges',
    'CDC_Support_Needed': 'sample cdc support needed',
    'Parent_File' : 'sample parent file'
}]

# insert data into db with given table and data
sql_connection.insert(table, data)
#sql_connection.insert(table_activities, data_activities)
#print('Last executed id', sql_connection.get_latest_projectID())
#print(sql_connection.get_latest_projectID())

# close the connection
sql_connection.close_connection()