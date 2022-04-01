from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
import mysql.connector


app = Flask(__name__)
app.secret_key = 'Secret Key'
#app.config['SQLALCHEMTY_DATABASE_URI'] = 'mysql://root:""@localhost/cs3311'
#app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

#db = SQLAlchemy(app)

#class Data(db.model):
#    id = db.Column(db.Integer)
#DB_HOST = '127.0.0.1'
#DB_NAME = 'CS3311'
#DB_USER = 'cs3311_admin'
#DB_PASS = 'password'
config = {
    'user': 'root',
    'password': '1100279464',
    'host': '127.0.0.1',
    'database': 'CS3311'
}

insert_query = {
    'projects': ("INSERT INTO projects "
            "(Project, State, Budget_Period_Start, Budget_Period_End, Reporting_Period) "
            "VALUES (%(Project)s, %(State)s, %(Budget_Period_Start)s, %(Budget_Period_End)s, %(Reporting_Period)s);"),
    'activities': ("INSERT INTO activities "
            "(ProjectID, Activity, Description, Outcome, Output, Timeline, Statistics, Status, Successes, Challenges, CDC_Support_Needed, Parent_File) "
            "VALUES (%(ProjectID)s, %(Activity)s, %(Description)s, %(Outcome)s, %(Output)s, %(Timeline)s, %(Statistics)s, %(Status)s, %(Successes)s, %(Challenges)s, %(CDC_Support_Needed)s, %(Parent_File)s);")
}

cnx = mysql.connector.connect(**config)
cursor = cnx.cursor()

@app.route("/")

def Index():
    s = "Select * FROM cs3311.activities"
    cursor.execute(s)
    list_activities = cursor.fetchall()
    return render_template("Index.html", activities = list_activities)

@app.route('/insert', methods = ['POST'])
def insert():
    if request.method =='POST':
        activity = request.form['Activity']
        description = request.form['Description']
        outcome = request.form['Outcome']
        output = request.form['Output']
        timeline = request.form['Timeline']
        statistics = request.form['Statistics']
        status = request.form['Status']
        successes = request.form['Successes']
        challenges = request.form['Challenges']
        CDC_Support_Needed = request.form['CDC_Support_Needed']
        Parent_File = request.form['Parent_File']

        table_activities = 'activities'

        data_activities = [{
            'ActivityID': 3,
            'ProjectID': 3,
            'Activity': activity,
            'Description': description,
            'Outcome': outcome,
            'Output' : output,
            'Timeline': timeline,
            'Statistics': statistics,
            'Status': status,
            'Successes': successes,
            'Challenges': challenges,
            'CDC_Support_Needed': CDC_Support_Needed,
            'Parent_File' : Parent_File
        }]

        if table_activities in insert_query:
            cursor.executemany(insert_query[table_activities], data_activities)
            cnx.commit()
        
        flash("Activity Inserted Successfully")

        return redirect(url_for('Index'))

@app.route('/Change Page')
def change():
    return render_template('index_project.html')


@app.route('/update', methods = ['GET', 'POST'])
def update():
    if request.method == 'POST':
        id = request.form.get('ActivityID')
        query = "Select * FROM cs3311.activities WHERE ActivityID = %s"
        #value = (int(id),)
        #value = (int(id))
        #cursor.execute(s)
        cursor.execute(query, (id, ))
        rel_activities = cursor.fetchall()
        print(rel_activities)
        activityID = rel_activities[0][0]
        print(activityID)

        activity = request.form['Activity']
        description = request.form['Description']
        outcome = request.form['Outcome']
        output = request.form['Output']
        timeline = request.form['Timeline']
        statistics = request.form['Statistics']
        status = request.form['Status']
        successes = request.form['Successes']
        challenges = request.form['Challenges']
        CDC_Support_Needed = request.form['CDC_Support_Needed']
        Parent_File = request.form['Parent_File']

        sql = """
        UPDATE activities
        SET Activity = %s,
            Description = %s,
            Outcome = %s,
            Output = %s,
            Timeline = %s,
            Statistics = %s,
            Status = %s,
            Successes = %s,
            Challenges = %s,
            CDC_Support_Needed = %s,
            Parent_File = %s
        WHERE ActivityID = %s
        """        
        cursor.execute(sql, (str(activity), str(description), str(outcome), str(output), str(timeline), str(statistics), 
                        str(status), str(successes), str(challenges), str(CDC_Support_Needed), str(Parent_File), activityID))
        cnx.commit()

        flash("Activity Updated Successfully")

        return redirect(url_for('Index'))

@app.route('/delete/<ActivityID>/', methods = ['GET', 'POST'])
def delete(ActivityID):
    sql = "DELETE FROM activities WHERE ActivityID = %s"
    cursor.execute(sql, (ActivityID,))
    cnx.commit()
    flash("Activity Deleted")
    return redirect(url_for('Index'))


if(__name__) == "__main__":
    app.run(host='localhost', port=1000, debug=True)
